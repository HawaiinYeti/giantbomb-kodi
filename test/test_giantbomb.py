import resources.lib.giantbomb as giantbomb
import time
import unittest


class TestGiantBombAPI(unittest.TestCase):
    def setUp(self):
        self.gb = giantbomb.GiantBomb()

    def test_categories(self):
        data = self.gb.query('video_types')

        self.assertIsInstance(data['number_of_total_results'], int)
        self.assertEqual(data['number_of_total_results'],
                          data['number_of_page_results'])
        self.assertEqual(data['number_of_page_results'], len(data['results']))

        for video_type in data['results']:
            self.assertIsInstance(video_type['name'], str)
            self.assertIsInstance(video_type['id'], int)

    def test_videos(self):
        data = self.gb.query('videos')

        self.assertEqual(data['number_of_page_results'], 100)
        self.assertEqual(data['number_of_page_results'], len(data['results']))

        for video in data['results']:
            self.assertIsInstance(video['name'], str)
            self.assertIsInstance(video['deck'], str)
            self.assertIsInstance(video['length_seconds'], int)

            self.assertIsInstance(video['publish_date'], str)
            time.strptime(video['publish_date'], '%Y-%m-%d %H:%M:%S')

            self.assertIsInstance(video['image']['super_url'], str)
            self.assertIsInstance(video['high_url'], str)

    def test_latest(self):
        default = self.gb.query('videos')
        desc = self.gb.query('videos', { 'sort': 'publish_date:desc' })

        for expectedvid, actualvid in zip(default['results'], desc['results']):
            for key, expected in iter(expectedvid['image'].items()):
                actual = actualvid['image'][key]
                if actual[0] == '/':
                    actual = 'http://static.giantbomb.com' + actual
                if expected[0] == '/':
                    expected = 'http://static.giantbomb.com' + expected
                self.assertEqual(actual, expected)
