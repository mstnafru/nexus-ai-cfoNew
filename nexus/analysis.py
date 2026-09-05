"""Risk and portfolio analysis for NEXUS."""

from dataclasses import dataclass
from typing import Dict, List
from .data import MarketData


@dataclass
class AssetInsight:
    symbol: str
    price: float
    volatility_pct: float
    trend: str
    drawdown_pct: float
    weight: float = 0.0
    flags: List[str] = None

    def __post_init__(self):
        if self.flags is None:
            self.flags = []


def analyze_asset(md: MarketData, risk_flags: dict) -> AssetInsight:
    price = md.price
    recent_high = max(md.highs)
    recent_low = min(md.lows)

    volatility_pct = ((recent_high - recent_low) / price) * 100 if price else 0.0
    drawdown_pct = (
        ((recent_high - price) / recent_high) * 100
        if recent_high else 0.0
    )

    first = md.closes[0]

    if price > first * 1.01:
        trend = "up"
    elif price < first * 0.99:
        trend = "down"
    else:
        trend = "flat"

    flags = []

    if volatility_pct >= risk_flags["high_volatility_pct"]:
        flags.append(
            f"high volatility ({volatility_pct:.1f}% range)"
        )

    if drawdown_pct >= risk_flags["drawdown_alert_pct"]:
        flags.append(
            f"down {drawdown_pct:.1f}% from recent high"
        )

    return AssetInsight(
        symbol=md.symbol,
        price=price,
        volatility_pct=volatility_pct,
        trend=trend,
        drawdown_pct=drawdown_pct,
        flags=flags,
    )


def analyze_portfolio(
    insights: List[AssetInsight],
    holdings: Dict[str, float],
    risk_flags: dict,
) -> dict:

    values = {
        i.symbol: i.price * holdings.get(i.symbol, 0.0)
        for i in insights
    }

    total = sum(values.values())

    weights = {
        sym: (value / total if total else 0.0)
        for sym, value in values.items()
    }

    portfolio_flags = []

    for insight in insights:
        insight.weight = weights.get(insight.symbol, 0.0)

    for sym, weight in weights.items():
        if weight >= risk_flags["max_concentration"]:
            portfolio_flags.append(
                f"{sym} concentration is {weight:.0%} "
                f"(limit {risk_flags['max_concentration']:.0%})"
            )

    candidates = []

    for i in insights:
        score = 0

        if i.weight >= risk_flags["max_concentration"]:
            score += 60 * i.weight

        score += min(i.drawdown_pct, 30) * 1.5
        score += min(i.volatility_pct, 30)

        if i.trend == "down":
            score += 10

        candidates.append((score, i))

    biggest_risk = max(
        candidates,
        key=lambda x: x[0],
        default=(0, None)
    )[1]

    return {
        "total_value": total,
        "values": values,
        "weights": weights,
        "flags": portfolio_flags,
        "biggest_risk": (
            biggest_risk
