import sys

from mock import patch
import requests

import bpc.http as http
from bpc.tests.tests import BaseTestCase, MockedResponse


class TestHTTPLib(BaseTestCase):

    @patch.object(requests, 'get', side_effect=Exception())
    def test_retry_on_requests_exception(self, mocked_requests):
        """Should retry when requests raises an exception"""
        with patch.object(http, 'retry_or_fail') as retry_mock:
            http.get('http://localhost')
            self.assertTrue(retry_mock.called)

    @patch.object(requests, 'get', return_value=MockedResponse(status_code=300))
    def test_retry_on_bad_status_code(self, mocked_requests):
        """Should retry when we get a response not in the 2xx range"""
        with patch.object(http, 'get') as retry_mock:
            http.get('http://localhost')
            self.assertTrue(retry_mock.called)

    @patch.object(requests, 'get', side_effect=Exception())
    def test_get_decrements_retries_left(self, mocked_requests):
        """Should decrement the number of retries left when retrying"""
        with patch.object(http, 'get') as get_mock:
            http.retry_or_fail('http://localhost', retries_left=4, stream=False)
            self.assertTrue(get_mock.called)
            get_mock.assert_called_with(
                'http://localhost', retries_left=3, stream=False)

    def test_exit_when_retries_exceeded(self):
        """Should exit when the retries limit has been reached"""
        with patch.object(sys, 'exit') as exit_mock:
            http.retry_or_fail('http://localhost', retries_left=0, stream=False)
            self.assertTrue(exit_mock.called)
