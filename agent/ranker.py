"""Simple, auditable priority heuristic, NOT factual verification."""
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SIGNALS = ("launch", "launched", "announced", "resmi", "confirmed", "regulation", "regulator", "security", "hack", "breach", "release", "rilis", "partnership", "acquisition", "funding", "update", "season", "trailer")
LOW_SIGNALS = ("rumor", "rumour", "could", "might", "prediction", "price target", "100x", "airdrop guaranteed")


def _hits(words, text):
    # Whole words only: "hack" must not match "hackathon".
    return sum(1 for w in words if re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", text))


def parse_published(value):
    """Accept RFC 822 (classic RSS) or ISO 8601 (Atom / what scan_feeds stores). Returns aware UTC datetime or None."""
    value = (value or "").strip()
    if not value:
        return None
    dt = None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = parsedate_to_datetime(value)
        except (ValueError, TypeError, OverflowError):
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def score(story, now=None) -> int:
    title = (story["title"] or "").lower()
    summary = (story["summary"] or "").lower()
    result = 30 + min(24, 8 * _hits(SIGNALS, title))
    result += min(8, 2 * _hits(SIGNALS, summary))
    result -= min(24, 12 * _hits(LOW_SIGNALS, title))
    if len(title) < 18: result -= 5
    dt = parse_published(story["published"])
    if dt:
        hours = ((now or datetime.now(timezone.utc)) - dt).total_seconds() / 3600
        if 0 <= hours <= 12: result += 18
        elif 0 <= hours <= 48: result += 9
    return max(0, min(100, result))
