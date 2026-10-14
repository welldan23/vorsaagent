"""Pure text helpers (no Telegram/IO dependencies) so they can be unit-tested."""
import html
import re
from urllib.parse import urlsplit, urlunsplit

TELEGRAM_LIMIT = 4096


def clean_text(s, limit=1000):
    """Strip tags and collapse ALL whitespace (incl. newlines) to one line."""
    s = re.sub(r"<[^>]+>", " ", str(s or ""))
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()[:limit]


def clean_multiline(s, limit=1000):
    """Like clean_text, but keeps line breaks (max one blank line in a row). For captions."""
    s = re.sub(r"<[^>]+>", " ", str(s or ""))
    s = html.unescape(s).replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[^\S\n]+", " ", line).strip() for line in s.split("\n")]
    s = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return s.strip()[:limit].rstrip()


def safe_url(url):
    try:
        u = urlsplit(url.strip())
        if u.scheme not in ("http", "https") or not u.hostname or u.username or u.password:
            return None
        # Feeds are configured locally; article URLs are only displayed, never fetched.
        return urlunsplit((u.scheme, u.netloc.lower(), u.path.rstrip("/") or "/", u.query, ""))
    except ValueError:
        return None


def chunk_lines(lines, limit=TELEGRAM_LIMIT - 96):
    """Join lines with newlines into as few messages as possible, each <= limit chars."""
    chunks, current = [], ""
    for line in lines:
        line = line[:limit]
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) > limit:
            chunks.append(current)
            current = line
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks
