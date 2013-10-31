import os
import unittest

import logbook


BASEDIR = os.path.abspath(os.path.dirname(__file__).replace('\\', '/'))

FIXTURES = {}

for filename in os.listdir(os.path.join(BASEDIR, 'fixtures')):
    with open(os.path.join(BASEDIR, 'fixtures', filename), 'r') as f:
        FIXTURES[filename] = f.read()


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.log_handler = logbook.TestHandler()
        self.log_handler.push_thread()
