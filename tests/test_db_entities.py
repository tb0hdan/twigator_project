import sys
sys.path.insert(1, ".")
sys.path.insert(2, "..")

import unittest

from twigator.db.connection import MongoConnection
from twigator.db.entities import Tweet

from tests import mytestrunner

class EntitiesTestCase(unittest.TestCase):
    '''
    '''
    def test_01_test_tweet_entity(self):
        with MongoConnection('mongoenginetest', host='mongomock://localhost'):
            tweet = Tweet(author_id=12345,
                          tweet_id=1234567890,
                          phrase='Sample tweet',
                          query_phrases=['news'],
                         )
            tweet.save()
            tweets = Tweet.objects().first()
            self.assertEqual(tweet.author_id, 12345)
            self.assertEqual(tweet.tweet_id, 1234567890)
            self.assertEqual(tweet.phrase, 'Sample tweet')
            self.assertEqual(tweet.query_phrases, ['news'])


if __name__ == '__main__':
    classes = [EntitiesTestCase]
    mytestrunner(classes)
