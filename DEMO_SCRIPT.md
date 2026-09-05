# 2-Minute Hackathon Demo

## 0:00 — Problem
"Crypto dashboards give me numbers. NEXUS tells me what those numbers mean for my portfolio."

## 0:20 — Show config
Show `config.yaml` and point out:
- BTC / ETH / BNB holdings
- 40% concentration limit
- 5% volatility alert
- 10% drawdown alert

## 0:40 — Run
```bash
python -m nexus.agent --config config.yaml --demo
```

## 1:00 — Explain the result
Point to:
- Portfolio value
- Priority asset
- RED/AMBER/GREEN severity
- WHY section
- Recommendation
- Workflow action

Say:
"NEXUS doesn't just flag ETH. It explains why the portfolio is exposed and turns the insight into a structured action."

## 1:30 — Workflow vision
"Today the action is a safe recommendation. The architecture can hand `CREATE_REBALANCE_PLAN`, `WATCH_VOLATILITY`, or other actions to a Trading, Payment, or Onchain workflow."

## 1:50 — Close
"NEXUS is the decision layer between raw market data and autonomous workflows."
