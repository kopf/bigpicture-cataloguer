from BeautifulSoup import BeautifulSoup
from mock import patch

from bpc.scraper import list_albums, list_album_photos, clean_caption_text
import bpc.http
from bpc.tests.tests import FIXTURES, BaseTestCase, MockedResponse


class TestScraper(BaseTestCase):

    @patch.object(bpc.http, 'get', return_value=MockedResponse(content=FIXTURES['2008-05.html']))
    def test_list_albums_old_site(self, mocked_get):
        """Should return a dictionary when parsing old (before sep 2008) months"""
        expected = [
            {'name': 'Uncontacted Tribe Photographed in Brazil',
                'url': 'http://www.boston.com/bigpicture/2008/05/uncontacted_tribe_photographed.html'},
            {'name': 'Cassini Nears Four-year Mark',
                'url': 'http://www.boston.com/bigpicture/2008/05/cassini_nears_fouryear_mark.html'}
        ]
        self.assertEqual(expected, list_albums(2008, 8))

    @patch.object(bpc.http, 'get', return_value=MockedResponse(content=FIXTURES['2008-09.html']))
    def test_list_albums_new_site(self, mocked_get):
        """Should return a dictionary when parsing newer (after sep 2008) months"""
        expected = [
            {'name': 'Childhood Cancer Awareness Month',
                'url': 'http://www.boston.com/bigpicture/2008/09/childhood_cancer_awareness_mon.html'},
            {'name': 'The Singapore Grand Prix',
                'url': 'http://www.boston.com/bigpicture/2008/09/the_singapore_grand_prix.html'}
        ]
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

    @patch.object(bpc.http, 'get',
        return_value=MockedResponse(content=FIXTURES['non_gallery.html']))
    def test_list_album_photos_non_gallery(self, mocked_get):
        """Should return an empty list when scraping a non-gallery page"""
        # e.g. http://www.boston.com/bigpicture/2008/10/a_quick_note_1.html
        self.assertEqual([], list_album_photos('bla'))

    @patch.object(bpc.http, 'get',
        return_value=MockedResponse(content=FIXTURES['youtube.html']))
    def test_list_album_photos_containing_youtube(self, mocked_get):
        """Should return a list of photos when the album contains an embedded youtube"""
        # e.g. http://www.boston.com/bigpicture/2008/10/nachtweys_wish_awareness_of_xd.html
        self.assertEqual(1, len(list_album_photos('bla')))

    @patch.object(bpc.http, 'get',
        return_value=MockedResponse(content=FIXTURES['removed_images.html']))
    def test_list_album_photos_removed_photos(self, mocked_get):
        """Should return a list of photos when the album contains removed photos"""
        # e.g. http://www.boston.com/bigpicture/2010/01/earthquake_in_haiti.html
        self.assertEqual(41, len(list_album_photos('bla')))

    def test_clean_caption_text(self):
        """Should clean up caption text"""
        caption = BeautifulSoup(u'  \xb4test \xd7\xb4\xa0&rsquo;an\xf2ther quote&rsquo; &copy;'
                                u' \xe1 <a href="bla">company</a> (24 photos total)  ')
        expected = u"'test x' 'another quote' Copyright a company"
        self.assertEqual(expected, clean_caption_text(caption))
