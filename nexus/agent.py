"""NEXUS command-line agent."""

import argparse
import yaml

from .data import fetch_watchlist_data, demo_market_data
from .analysis import analyze_asset, analyze_portfolio
from .decision import decide
from .report import build_report


def run_once(config: dict, demo: bool = False) -> str:
    market_data = (
        demo_market_data()
        if demo
        else fetch_watchlist_data(config["watchlist"])
    )

    insights = [
        analyze_asset(md, config["risk_flags"])
        for md in market_data
    ]

    portfolio = analyze_portfolio(
        insights,
        config["portfolio"],
        config["risk_flags"],
    )

    priority = next(
        (i for i in insights if i.symbol == portfolio["biggest_risk"]),
        insights[0] if insights else None,
    )

    if priority is None:
        raise RuntimeError("No market data available.")

    decision = decide(priority, portfolio, config)

    return build_report(
        config["report"]["title"],
        insights,
        portfolio,
        decision,
    )


def main():
    parser = argparse.ArgumentParser(
        description="NEXUS — Autonomous Crypto CFO"
    )
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--once", action="store_true")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="use offline deterministic demo data"
    )
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    report = run_once(config, demo=args.demo)
    print(report)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
