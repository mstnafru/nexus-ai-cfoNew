"""Explainable decision engine for NEXUS."""

from dataclasses import dataclass
from .analysis import AssetInsight


@dataclass
class Decision:
    severity: str
    headline: str
    why: str
    recommendation: str
    action: str


def decide(
    insight: AssetInsight,
    portfolio: dict,
    config: dict
) -> Decision:

    concentration_limit = config["risk_flags"]["max_concentration"]
    buffer = config["decision"]["rebalance_buffer_pct"] / 100

    if insight.weight >= concentration_limit:
        target = max(concentration_limit - buffer, 0)

        return Decision(
            severity="RED",
            headline=f"{insight.symbol} concentration is too high",
            why=(
                f"{insight.symbol} represents {insight.weight:.0%} "
                f"of the portfolio, above the configured "
                f"{concentration_limit:.0%} limit."
            ),
            recommendation=(
                f"Consider reducing {insight.symbol} toward "
                f"{target:.0%} portfolio weight."
            ),
            action="CREATE_REBALANCE_PLAN",
        )

    if insight.drawdown_pct >= config["risk_flags"]["drawdown_alert_pct"]:
        return Decision(
            severity="AMBER",
            headline=f"{insight.symbol} is in a significant drawdown",
            why=(
                f"The price is {insight.drawdown_pct:.1f}% "
                f"below its recent high."
            ),
            recommendation=(
                "Review position size and risk tolerance "
                "before adding exposure."
            ),
            action="REVIEW_POSITION",
        )

    if insight.volatility_pct >= config["risk_flags"]["high_volatility_pct"]:
        return Decision(
            severity="AMBER",
            headline=f"{insight.symbol} volatility is elevated",
            why=(
                f"The recent high-to-low range is "
                f"{insight.volatility_pct:.1f}% of the current price."
            ),
            recommendation=(
                "Treat new entries cautiously and review "
                "portfolio-level exposure."
            ),
            action="WATCH_VOLATILITY",
        )

    return Decision(
        severity="GREEN",
        headline=f"{insight.symbol} is within configured risk limits",
        why=(
            "No configured concentration, drawdown, or "
            "volatility alert was triggered."
        ),
        recommendation="Continue monitoring.",
        action="MONITOR",
    )
