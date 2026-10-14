# VORSA Agent Skills (v1)
- `scan`: read configured RSS feeds; deduplicate by canonical URL; save stories to SQLite.
- `latest`: list stored stories filtered by news/anime/crypto.
- `recommend`: score recent stored stories using transparent heuristic; this is prioritization, not fact-checking.
- `draft`: generate Indonesian headline and caption from RSS metadata using optional external LLM; otherwise mark as manual verification required.
- `revise`: edit an existing draft and invalidate any previous approval.
- `preview`: render 1080x1350 text-based editorial PNG (not a licensed news photograph).
- `approve`: record editor approval bound to current draft version; does not publish.
- `status`: show current draft, version, approval.
- `help`: explain commands.
Out of scope: autonomous browsing/fact checking, photo licensing, Instagram posting, financial advice.
