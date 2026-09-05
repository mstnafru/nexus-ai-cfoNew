from nexus.agent import run_once
import yaml

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

report = run_once(config, demo=True)
assert "NEXUS" in report
assert "Portfolio Breakdown" in report
assert "Recommendation" in report
print("NEXUS smoke test: PASS")
