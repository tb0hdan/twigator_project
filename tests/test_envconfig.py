import unittest

from twigator.envconfig import EnvConfig

from . import mytestrunner

class EnvConfigTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        self.dummy_empty_environment = {'X': 1}
        self.dummy_valid_environment = {'MONGO_HOST': 'example.com'}

    def test_01_empty_environment(self):
        env_config = EnvConfig(environment=self.dummy_empty_environment)
        self.assertEqual(env_config.MONGO_HOST, 'localhost')

    def test_02_valid_environment(self):
        env_config = EnvConfig(environment=self.dummy_valid_environment)
        self.assertEqual(env_config.MONGO_HOST, 'example.com')

    def tearDown(self):
        self.env_config = None


if __name__ == '__main__':
    classes = [DummyTestCase]
    mytestrunner(classes)
