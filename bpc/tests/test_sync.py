import os

from freezegun import freeze_time
from freezegun.api import FakeDatetime

from bpc.sync import get_latest, get_months, get_start_date, START
from bpc.tests.tests import BaseTestCase, BASEDIR


class TestGetLatest(BaseTestCase):

    def test_get_latest(self):
        """Should return highest number when called with list of number strings"""
        l = ['2009', '2010', '2011']
        self.assertEquals(get_latest(l), 2011)
        l = ['05', '06', '07']
        self.assertEqual(7, get_latest(l))

    def test_get_latest_with_unknown_files(self):
        """Should return highest number when called with list numbers and other files"""
        l = ['2009', '2010', '2011', 'Thumbs.db', '__MACOSX']
        self.assertEqual(2011, get_latest(l))


class TestSyncWithFixtureDirs(BaseTestCase):

    NON_EXISTANT_DIR = os.path.join(BASEDIR, 'this_dir_does_not_exist')
    EXISTANT_DIR = os.path.join(BASEDIR, 'bigpicture_photos')

    def setUp(self):
        super(TestSyncWithFixtureDirs, self).setUp()
        os.mkdir(self.EXISTANT_DIR)

    def tearDown(self):
        super(TestSyncWithFixtureDirs, self).tearDown()
        if os.path.exists(self.NON_EXISTANT_DIR):
            os.rmdir(self.NON_EXISTANT_DIR)
        os.rmdir(self.EXISTANT_DIR)

    def test_get_start_date_non_existant_dir(self):
        """Should return start date equal to BP's start date when dir doesn't exist"""
        path = os.path.join(BASEDIR, 'this_dir_does_not_exist')
        self.assertEqual(START, get_start_date(self.NON_EXISTANT_DIR))

    def test_get_start_date_empty_dir(self):
        """Should return start date equal to BP's start date when dir is empty"""
        self.assertEqual(START, get_start_date(self.EXISTANT_DIR))

    @freeze_time('2008-07-01')
    def test_get_months(self):
        """Should return a list of months to be downloaded"""
        months = get_months(self.EXISTANT_DIR)
        expected = [
            FakeDatetime(2008, 05, 01), FakeDatetime(2008, 06, 01), FakeDatetime(2008, 07, 01)
        ]
