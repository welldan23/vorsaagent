"""Simple, auditable priority heuristic, NOT factual verification."""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SIGNALS = ("launch", "launched", "announced", "resmi", "confirmed", "regulation", "regulator", "security", "hack", "breach", "release", "rilis", "partnership", "acquisition", "funding", "update", "season", "trailer")
LOW_SIGNALS = ("rumor", "rumour", "could", "might", "prediction", "price target", "100x", "airdrop guaranteed")

def score(story) -> int:
    title = (story["title"] or "").lower()
    summary = (story["summary"] or "").lower()
    result = 30 + min(24, sum(8 for word in SIGNALS if word in title))
    result += min(8, sum(2 for word in SIGNALS if word in summary))
    result -= min(24, sum(12 for word in LOW_SIGNALS if word in title))
    if len(title) < 18: result -= 5
    try:
        dt = parsedate_to_datetime(story["published"])
        if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
        hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
        if 0 <= hours <= 12: result += 18
        elif 0 <= hours <= 48: result += 9
    except (ValueError, TypeError, OverflowError):
        pass
    return max(0, min(100, result))
