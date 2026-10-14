"""DB / draft / approval / preview tests. Needs requirements.txt installed (imports bot.py)."""
import io
import os
import tempfile
import unittest

_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "test.sqlite3")

import bot  # noqa: E402  (must import after DB_PATH is set)
from PIL import Image  # noqa: E402


class BotDbTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bot.setup_db()
        with bot.connect() as db:
            cur = db.execute("INSERT INTO stories(vertical,title,url,source,summary,published,created_at) VALUES(?,?,?,?,?,?,?)",
                             ("news", "A test headline", "https://example.com/a", "Example", "", "", bot.now()))
            cls.sid = cur.lastrowid

    def test_connect_commits_and_closes(self):
        with bot.connect() as db:
            db.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('k','v')")
        with self.assertRaises(Exception):
            db.execute("SELECT 1")  # closed
        with bot.connect() as db:
            self.assertEqual(db.execute("SELECT value FROM meta WHERE key='k'").fetchone()["value"], "v")

    def test_revision_invalidates_approval(self):
        v1 = bot.save_draft(self.sid, "Judul", "Caption\n\nbaris dua", actor=1)
        with bot.connect() as db:
            db.execute("UPDATE drafts SET approved_version=?, approved_at=? WHERE story_id=?", (v1, bot.now(), self.sid))
        self.assertEqual(bot.draft_by_id(self.sid)["approved_version"], v1)
        v2 = bot.save_draft(self.sid, "Judul baru", "Caption baru", actor=1)
        self.assertEqual(v2, v1 + 1)
        d = bot.draft_by_id(self.sid)
        self.assertIsNone(d["approved_version"])
        self.assertEqual(d["caption"], "Caption baru")

    def test_render_preview(self):
        bot.save_draft(self.sid, "Sebuah headline yang cukup panjang untuk dibungkus ke beberapa baris " * 3, "c", actor=1)
        png = bot.render_preview(bot.story_by_id(self.sid), bot.draft_by_id(self.sid))
        self.assertEqual(Image.open(io.BytesIO(png)).size, (1080, 1350))

    def test_font_fallback_without_ttf(self):
        saved = bot.FONT_CANDIDATES
        try:
            bot.FONT_CANDIDATES = {True: ["/nonexistent.ttf"], False: ["/nonexistent.ttf"]}
            ft = bot.font(40, True)
            self.assertEqual(ft.size, 40)
            png = bot.render_preview(bot.story_by_id(self.sid), {"headline": "Tanpa font TTF", "version": 1})
            self.assertTrue(png.startswith(b"\x89PNG"))
        finally:
            bot.FONT_CANDIDATES = saved


if __name__ == "__main__":
    unittest.main()
