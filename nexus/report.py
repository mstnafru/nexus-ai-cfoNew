"""Human-readable CFO report generation."""

from .decision import Decision
from .analysis import AssetInsight


def build_report(
    title: str,
    insights: list[AssetInsight],
    portfolio: dict,
    decision: Decision,
) -> str:

    lines = [
        f"# {title}",
        "",
        "## Executive Summary",
        "",
        f"**Portfolio value:** ${portfolio['total_value']:,.2f}",
        f"**Priority asset:** {portfolio['biggest_risk'] or 'None'}",
        f"**Decision severity:** {decision.severity}",
        "",
        f"### {decision.headline}",
        decision.why,
        "",
        f"**Recommendation:** {decision.recommendation}",
        f"**Workflow action:** `{decision.action}`",
        "",
        "## Portfolio Breakdown",
        "",
        "| Asset | Price | Trend | Volatility | Drawdown | Weight |",
        "|---|---:|:---:|---:|---:|---:|",
    ]

    for i in insights:
        lines.append(
            f"| {i.symbol} | ${i.price:,.2f} | {i.trend} | "
            f"{i.volatility_pct:.1f}% | {i.drawdown_pct:.1f}% | "
            f"{i.weight:.0%} |"
        )

    lines += [
        "",
        "## Flagged Insights",
        "",
    ]

    flags = list(portfolio["flags"])

    for i in insights:
        flags.extend(
            f"{i.symbol}: {flag}"
            for flag in i.flags
        )

    if flags:
        lines.extend(
            f"- ⚠️ {flag}"
            for flag in flags
        )
    else:
        lines.append("- None")

    lines += [
        "",
        "## CFO Reasoning",
        "",
        "NEXUS prioritizes concentration first, then drawdown "
        "and volatility, so the report focuses attention on "
        "the risk with the highest potential portfolio impact.",
        "",
        "> Demo only: recommendations are informational and "
        "no financial transaction is executed.",
    ]

    return "\n".join(lines)
