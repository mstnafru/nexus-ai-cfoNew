# NEXUS — Autonomous Crypto CFO

NEXUS turns live crypto market + portfolio data into explainable risk decisions and actionable workflow recommendations.

## Track
**Data & Analysis** — with extension points for Trading, Payment, and Onchain workflows.

## Flow

Market Data → Risk Engine → Decision Engine → CFO Brief → Optional Action

## What it analyzes
- Current price
- Recent high / drawdown
- Recent trading range as a volatility proxy
- Portfolio value and concentration
- Portfolio-level risk flags
- A priority score for the most important issue

## Run

```bash
pip install -r requirements.txt
python -m nexus.agent --config config.yaml --once
```

Use deterministic demo data without network access:

```bash
python -m nexus.agent --config config.yaml --demo
```

Write the report to a file:

```bash
python -m nexus.agent --config config.yaml --demo --out report.md
```

## Demo story

Ask: "Why am I taking too much risk?"

NEXUS identifies the highest-impact portfolio issue, explains the reason, and proposes a concrete next action. It does not place trades automatically in this demo.

## Safety

This project is an analysis/recommendation demo. It does not execute trades, transfers, staking, or DeFi transactions.
