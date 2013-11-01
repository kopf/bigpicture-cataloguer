from mock import patch

from bpc.scraper import list_albums, list_album_photos
import bpc.http
from bpc.tests.tests import FIXTURES, BaseTestCase, MockedResponse


class TestScraper(BaseTestCase):

    @patch.object(bpc.http, 'get', return_value=MockedResponse(content=FIXTURES['2008-05.html']))
    def test_list_albums_old_site(self, mocked_get):
        """Should return a dictionary when parsing old (before sep 2008) months"""
        expected = {
            'Cassini Nears Four-year Mark': 
                'http://www.boston.com/bigpicture/2008/05/cassini_nears_fouryear_mark.html',
            'Uncontacted Tribe Photographed in Brazil': 
                'http://www.boston.com/bigpicture/2008/05/uncontacted_tribe_photographed.html'
        }
        self.assertEqual(expected, list_albums(2008, 8))

    @patch.object(bpc.http, 'get', return_value=MockedResponse(content=FIXTURES['2008-09.html']))
    def test_list_albums_new_site(self, mocked_get):
        """Should return a dictionary when parsing newer (after sep 2008) months"""
        expected = {
            'The Singapore Grand Prix':
                'http://www.boston.com/bigpicture/2008/09/the_singapore_grand_prix.html',
            'Childhood Cancer Awareness Month':
                'http://www.boston.com/bigpicture/2008/09/childhood_cancer_awareness_mon.html'
        }
        self.assertEqual(expected, list_albums(2008, 9))

    @patch.object(bpc.http, 'get',
        return_value=MockedResponse(content=FIXTURES['cassini_nears_fouryear_mark.html']))
    def test_list_album_photos(self, mocked_get):
        """Should return a list of photos when given a photo album url"""
        expected = [
            {'caption': (u"NASA's Cassini Spacecraft is now reaching the end of its four-year prime mission "
                          "(on June 30th), and about to enter into its extended mission. What a nice excuse "
                          "for a retrospective of some of the great images sent back home by Cassini over "
                          "the past four years. || The Sun is on the opposite side, so all of Saturn is "
                          "backlit. Courtesy NASA/JPL-Caltech"),
             'url': u'http://cache.boston.com/universal/site_graphics/blogs/bigpicture/saturn_05_30/cassini1.jpg'},
            {'caption': u"Swirls in Saturn's cloud-tops. Courtesy NASA/JPL-Caltech",
             'url': u'http://cache.boston.com/universal/site_graphics/blogs/bigpicture/saturn_05_30/cassini2.jpg'},
            {'caption': u"The surface of Saturn's moon Dione, up close. Courtesy NASA/JPL-Caltech",
             'url': u'http://cache.boston.com/universal/site_graphics/blogs/bigpicture/saturn_05_30/cassini3.jpg'},
        ]
        self.assertEqual(expected, list_album_photos('bla'))

    @patch.object(bpc.http, 'get',
        return_value=MockedResponse(content=FIXTURES['round_trip_with_endeavour.html']))
    def test_list_newer_album_photos(self, mocked_get):
        """Should return a list of photos when given a recent photo album url"""
        expected = [
            {'caption': 'intro || photo 1 caption',
             'url': u'pic1.jpg'},
            {'caption': u"photo 2 caption",
             'url': u'pic2.jpg'},
            {'caption': u"photo 3 caption",
             'url': u'pic3.jpg'},
        ]
        self.assertEqual(expected, list_album_photos('bla'))
