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

    @patch.object(bpc.http, 'get', return_value=FIXTURES['2008-09.html'])
    def test_get_albums_new_site(self, mocked_get):
        """Should return a dictionary when parsing newer (after sep 2008) months"""
        expected = {
            'The Singapore Grand Prix':
                'http://www.boston.com/bigpicture/2008/09/the_singapore_grand_prix.html',
            'Childhood Cancer Awareness Month':
                'http://www.boston.com/bigpicture/2008/09/childhood_cancer_awareness_mon.html'
        }
        self.assertEqual(expected, get_albums(2008, 9))
