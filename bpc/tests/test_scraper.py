import unittest

from mock import patch

from bpc.scraper import get_albums
import bpc.http
from bpc.tests.tests import FIXTURES


class TestScraper(unittest.TestCase):
    @patch.object(bpc.http, 'get', return_value=FIXTURES['2008-05.html'])
    def test_get_albums_old_site(self, mocked_get):
        """Should return a dictionary when parsing old (before sep 2008) months"""
        expected = {
            'Cassini Nears Four-year Mark': 
                'http://www.boston.com/bigpicture/2008/05/cassini_nears_fouryear_mark.html',
            'Uncontacted Tribe Photographed in Brazil': 
                'http://www.boston.com/bigpicture/2008/05/uncontacted_tribe_photographed.html'
        }
        self.assertEqual(expected, get_albums(2008, 8))
