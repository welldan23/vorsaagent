"""Conservative deterministic Indonesian natural-language routing.
No LLM may trigger approval or publication through a generated tool call.
"""
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Intent:
    action: str
    vertical: str = ""
    story_id: int | None = None

VERTICALS = {
    "anime": ("anime", "manga", "wibu", "otaku", "jepang"),
    "crypto": ("crypto", "kripto", "bitcoin", "btc", "web3", "defi", "onchain", "on-chain"),
    "news": ("news", "berita umum", "dunia", "teknologi", "politik"),
}

def route(text: str) -> Intent:
    t = text.lower().strip()
    vertical = next((k for k, words in VERTICALS.items() if any(re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t) for w in words)), "")
    match = re.search(r"(?:#|(?:berita|draft|post|artikel|id)\s*)(\d{1,8})\b", t)
    sid = int(match.group(1)) if match else None
    if re.search(r"\b(approve|setujui|publish|posting|terbitkan)\b", t):
        return Intent("approval_guidance", vertical, sid)  # Never approve via ambiguous natural language
    if re.search(r"\b(preview|pratinjau|desain|gambar)\b", t):
        return Intent("preview", vertical, sid)
    if re.search(r"\b(revisi|ubah|edit|ganti)\b", t):
        return Intent("edit_guidance", vertical, sid)
    if re.search(r"\b(draft|caption|headline|judul|bikinin postingan|buat postingan)\b", t):
        return Intent("draft", vertical, sid)
    if re.search(r"\b(scan|pantau|refresh|cek rss|ambil rss)\b", t):
        return Intent("scan", vertical, sid)
    if re.search(r"\b(rekomendasi|penting|menarik|prioritas|pilihin|pilih berita)\b", t):
        return Intent("recommend", vertical, sid)
    if re.search(r"\b(berita|terbaru|hari ini|update|cariin|carikan|latest)\b", t):
        return Intent("latest", vertical, sid)
    return Intent("help", vertical, sid)
