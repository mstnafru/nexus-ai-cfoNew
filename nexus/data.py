"""Market-data ingestion for NEXUS."""

from dataclasses import dataclass
from typing import List
import json
import urllib.parse
import urllib.request


BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


@dataclass
class MarketData:
    symbol: str
    closes: List[float]
    highs: List[float]
    lows: List[float]

    @property
    def price(self) -> float:
        return self.closes[-1]


def fetch_market_data(symbol: str, limit: int = 50, interval: str = "1h") -> MarketData:
    params = urllib.parse.urlencode(
        {"symbol": symbol, "interval": interval, "limit": limit}
    )
    url = f"{BINANCE_KLINES_URL}?{params}"

    with urllib.request.urlopen(url, timeout=10) as resp:
        raw = json.loads(resp.read())

    return MarketData(
        symbol=symbol,
        closes=[float(c[4]) for c in raw],
        highs=[float(c[2]) for c in raw],
        lows=[float(c[3]) for c in raw],
    )


def fetch_watchlist_data(watchlist: List[str]) -> List[MarketData]:
    results = []
    for symbol in watchlist:
        try:
            results.append(fetch_market_data(symbol))
        except Exception as exc:
            print(f"[warn] could not fetch {symbol}: {exc}")
    return results


def demo_market_data() -> List[MarketData]:
    """Offline deterministic data for a hackathon demo."""
    return [
        MarketData(
            "BTCUSDT",
            [94000, 94800, 95500, 96200, 97000, 97800, 98500, 99200],
            [95000, 96000, 97000, 98000, 99000, 99500, 100000, 100200],
            [93000, 94000, 94800, 95500, 96500, 97200, 98000, 98500],
        ),
        MarketData(
            "ETHUSDT",
            [3800, 3750, 3700, 3650, 3600, 3500, 3450, 3400],
            [3850, 3820, 3760, 3720, 3670, 3580, 3520, 3460],
            [3740, 3650, 3600, 3500, 3440, 3380, 3300, 3260],
        ),
        MarketData(
            "BNBUSDT",
            [700, 705, 710, 708, 712, 715, 718, 720],
            [708, 713, 715, 716, 720, 723, 725, 725],
            [695, 700, 704, 702, 706, 710, 712, 714],
        ),
    ]
