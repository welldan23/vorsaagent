import unittest
from datetime import datetime, timezone
from agent.router import route
from agent.ranker import parse_published, score
from agent.textutil import chunk_lines, clean_multiline, clean_text, safe_url

class AgentTests(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(route('cariin berita anime terbaru').action, 'latest')
        self.assertEqual(route('rekomendasi crypto').vertical, 'crypto')
        self.assertEqual(route('bikinin draft berita #12').story_id, 12)
        self.assertEqual(route('approve berita #12').action, 'approval_guidance')
        self.assertEqual(route('preview berita #12').action, 'preview')
    def test_route_story_id_ignores_durations(self):
        self.assertIsNone(route('bikinin draft berita 5 menit lalu').story_id)
        self.assertIsNone(route('berita 2 jam terakhir soal bitcoin').story_id)
        self.assertEqual(route('bikinin draft berita 12').story_id, 12)
        self.assertEqual(route('draft #7 dong').story_id, 7)
    def test_ranking(self):
        base = {'summary':'', 'published':''}
        self.assertGreater(score({**base,'title':'Official launch announced today'}), score({**base,'title':'Rumor: could be 100x'}))
    def test_ranking_whole_words(self):
        base = {'summary':'', 'published':''}
        self.assertEqual(score({**base,'title':'Students join a big hackathon event'}), score({**base,'title':'Students join a big cooking event'}))
        self.assertGreater(score({**base,'title':'Exchange hack drains wallets'}), score({**base,'title':'Exchange news drains wallets'}))
    def test_ranking_recency_rfc822_and_iso(self):
        now = datetime(2026, 10, 14, 12, 0, tzinfo=timezone.utc)
        base = {'title':'Some ordinary headline here', 'summary':''}
        old = score({**base, 'published':''}, now=now)
        self.assertEqual(score({**base, 'published':'Wed, 14 Oct 2026 08:00:00 GMT'}, now=now), old + 18)
        self.assertEqual(score({**base, 'published':'2026-10-14T08:00:00+00:00'}, now=now), old + 18)
        self.assertEqual(score({**base, 'published':'2026-10-13T00:00:00Z'}, now=now), old + 9)
        self.assertIsNone(parse_published('not a date'))

class TextUtilTests(unittest.TestCase):
    def test_clean_multiline_keeps_paragraphs(self):
        raw = "Paragraf <b>1</b>\r\n\r\n\r\n\r\nParagraf   2 &amp; lanjut\n#vorsa"
        self.assertEqual(clean_multiline(raw), "Paragraf 1\n\nParagraf 2 & lanjut\n#vorsa")
        self.assertEqual(clean_text(raw), "Paragraf 1 Paragraf 2 & lanjut #vorsa")
    def test_safe_url(self):
        self.assertEqual(safe_url('HTTPS://Example.COM/a/b/?x=1#frag'), 'https://example.com/a/b?x=1')
        self.assertIsNone(safe_url('javascript:alert(1)'))
        self.assertIsNone(safe_url('https://user:pw@example.com/'))
    def test_chunk_lines(self):
        lines = ['x' * 1500 for _ in range(6)]
        chunks = chunk_lines(lines, limit=4000)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(all(len(c) <= 4000 for c in chunks))
        self.assertEqual('\n'.join(chunks), '\n'.join(lines))
        self.assertEqual(chunk_lines(['a', 'b']), ['a\nb'])

if __name__ == '__main__': unittest.main()
