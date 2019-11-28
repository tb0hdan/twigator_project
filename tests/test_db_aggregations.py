import sys
sys.path.insert(1, ".")
sys.path.insert(2, "..")

import unittest
from mongoengine import connect, disconnect
from twigator.db.aggregations import (
                                      get_top_hashtags,
                                      get_tweet_count,
                                      get_top_twitters)
from tests import mytestrunner

class AggregationsTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

    def test_01_test_top_hashtags(self):
        print(get_top_hashtags())

    def test_02_get_tweet_count(self):
        print(get_tweet_count())

    def test_03_get_top_twitters(self):
        print(get_top_twitters())

    def tearDown(self):
        disconnect()


if __name__ == '__main__':
    classes = [AggregationsTestCase]
    mytestrunner(classes)
