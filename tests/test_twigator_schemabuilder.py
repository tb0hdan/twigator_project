import os
import unittest

from twigator.schemabuilder import get_schema

from . import mytestrunner

class SchemaBuilderTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        self.fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'schema.yml')

    def test_01_test_normal(self):
        fixture_data = open(self.fixture, 'r').read().rstrip('\n')
        generated_data = get_schema().rstrip('\n')
        self.assertEqual(fixture_data, generated_data)


if __name__ == '__main__':
    classes = [DummyTestCase]
    mytestrunner(classes)
