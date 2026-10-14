import unittest
from agent.router import route
from agent.ranker import score

class AgentTests(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(route('cariin berita anime terbaru').action, 'latest')
        self.assertEqual(route('rekomendasi crypto').vertical, 'crypto')
        self.assertEqual(route('bikinin draft berita #12').story_id, 12)
        self.assertEqual(route('approve berita #12').action, 'approval_guidance')
        self.assertEqual(route('preview berita #12').action, 'preview')
    def test_ranking(self):
        base = {'summary':'', 'published':''}
        self.assertGreater(score({**base,'title':'Official launch announced today'}), score({**base,'title':'Rumor: could be 100x'}))
if __name__ == '__main__': unittest.main()
