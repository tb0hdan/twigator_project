import unittest

from mongoengine import connect, disconnect
from twigator.db.entities import Tweet
from twigator.db.queries import (
                                 get_last_tweets,
                                 get_tweet_by_id,
                                 get_author_by_id
                                )

from . import mytestrunner

class QueriesTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        tweet = Tweet(author_id=12345,
                      tweet_id=1234567890,
                      phrase='Sample tweet',
                      query_phrases=['news'],
                     )
        tweet.save()

    def test_01_test_get_last_tweets(self):
        print(get_last_tweets())

    def test_02_test_get_tweet_by_id(self):
        print(get_tweet_by_id(1234567890))

    def test_01_test_author_by_id(self):
        print(get_author_by_id(12345))

    def tearDown(self):
        disconnect()


if __name__ == '__main__':
    classes = [DummyTestCase]
    mytestrunner(classes)
