# VORSA AI Newsroom — Agent v1

Telegram-first modular-agent MVP for **@vorsa.news**, **@vorsa.anime**, and **@vorsa.crypto**.

## Current architecture
- `bot.py`: Telegram handlers (aiogram 3), RSS ingestion (HTTPX + feedparser), APScheduler 15-minute background scans, SQLite story/draft/approval storage, OpenAI-compatible API drafting, Pillow 1080x1350 previews. Still a modular monolith, **not** microservices.
- `agent/router.py`: conservative Indonesian natural-language intent router; never approves via natural language.
- `agent/ranker.py`: auditable heuristic story shortlist; **not** fact-checking.
- `agent/SOUL.md` / `agent/SKILL.md`: editorial policy and documented capabilities (human-readable; not dynamically loaded by LLM yet).
- `brands/*.json`: brand identities for future per-brand templates.
- `feeds.json`: editable RSS feed list.

## Install on Ubuntu 22.04+ / Python 3.10+
```bash
sudo apt update && sudo apt install -y python3 python3-venv unzip
unzip vorsa_agent_v1.zip
cd vorsa_agent_v1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python bot.py
```
Create Telegram bot token via @BotFather. Get numeric Telegram user ID from a trusted ID bot or Telegram API. Set `ADMIN_TELEGRAM_IDS` to your ID (comma-separated if more than one). Keep `.env` private and never commit it. `OPENAI_API_KEY` optional: without it, drafts are marked manual verification required.

## Usage
- `/start`, `/scan`, `/latest [news|anime|crypto]`, `/recommend [news|anime|crypto]`
- `/draft 12`, `/preview 12`, `/edit 12 | Headline | Caption`, `/approve 12`, `/status 12`
- Natural chat examples: `cariin berita anime terbaru`, `rekomendasi crypto`, `bikinin draft berita #12`, `preview berita #12`.
- Natural language **never** triggers approval. `/approve ID` only records approval, never publishes.

## Safety and limitations
- RSS is fetched from locally configured sources; article URLs are displayed, not fetched.
- RSS is untrusted. Drafts are based on RSS metadata and are **not independently fact-checked**.
- Scoring is heuristic, not an LLM evaluation.
- No automated photo search, licensed imagery, Instagram/Meta API publishing, full autonomous browsing, multi-turn tool-using LLM, or scheduled publication.
- Initial feed scan seeds the database without alerting old headlines; subsequent scans alert new ones.
- Only allowlisted Telegram IDs in private chats can access bot commands.
- No external credentials are bundled; live Telegram/API execution not tested here.

## Tests
```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

## Running as service
Edit `vorsa.service` paths/user for your server, then copy to `/etc/systemd/system/vorsa.service` and enable with `sudo systemctl daemon-reload && sudo systemctl enable --now vorsa`.

## Next production steps
Separate newsroom and publishing modules, add URL and feed trust controls, source corroboration, media licensing workflow, Telegram inline approval buttons with version-bound confirmation, structured LLM tool calling with strict permissions, monitoring/backups, and official Meta API integration only after app review/permissions are ready.
