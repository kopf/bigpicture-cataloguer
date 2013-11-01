import os
import unittest

import logbook
import requests


BASEDIR = os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))

FIXTURES = {}

for filename in os.listdir(os.path.join(BASEDIR, 'fixtures')):
    with open(os.path.join(BASEDIR, 'fixtures', filename), 'r') as f:
        FIXTURES[filename] = f.read()


class MockedResponse(requests.Response):

    def __init__(self, status_code=200, content=''):
        super(MockedResponse, self).__init__()
        self.status_code = status_code
        self._content = content


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
