import unittest
from unittest.mock import Mock, MagicMock

import twython

EXPECTED_STATUSES = ['1']

mocked_search = MagicMock()
mocked_search.search.return_value = {'statuses': EXPECTED_STATUSES}
twython.Twython = Mock(return_value=mocked_search)

from mongoengine import connect, disconnect

from twigator.db.entities import Tweet
from twigator.worker import get_statuses, add_to_db, runner

from . import mytestrunner


class WorkerTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

    def test_01_test_get_statuses(self):
        statuses = get_statuses(1, 2, 3, 4)
        self.assertEqual(statuses, EXPECTED_STATUSES)

    def test_02_test_add_to_db(self):
        add_to_db([{'id': 12345, 'created_at': 'Thu Aug 29 13:05:24 +0000 2019',
                    'text': 'lorem ipsum'}], 'news')
        tweet = Tweet.objects().first()
        self.assertEqual(tweet.tweet_id, 12345)

    def tearDown(self):
        disconnect()

if __name__ == '__main__':
    classes = [DummyTestCase]
    mytestrunner(classes)
