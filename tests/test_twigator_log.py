import sys
sys.path.insert(1, ".")
sys.path.insert(2, "..")

import unittest

from twigator.log import logger

from tests import mytestrunner

class LoggerTestCase(unittest.TestCase):
    '''
    '''
    def test_01_info(self):
        self.assertEqual(hasattr(logger, 'info'), True)

    def test_02_warning(self):
        self.assertEqual(hasattr(logger, 'warning'), True)

    def test_03_error(self):
        self.assertEqual(hasattr(logger, 'error'), True)


if __name__ == '__main__':
    classes = [LoggerTestCase]
    mytestrunner(classes)
