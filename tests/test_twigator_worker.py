import sys
sys.path.insert(1, ".")
sys.path.insert(2, "..")

import unittest
from unittest.mock import Mock, MagicMock

import twython

EXPECTED_STATUSES = [{'id': 23456, 'created_at': 'Thu Aug 29 13:05:24 +0000 2011',
                    'text': 'lorem'}]

mocked_search = MagicMock()
mocked_search.search.return_value = {'statuses': EXPECTED_STATUSES}
twython.Twython = Mock(return_value=mocked_search)


from mongoengine import connect, disconnect

from twigator.db.entities import Tweet
from twigator.worker import get_statuses, add_to_db, runner


from tests import mytestrunner


class WorkerTestCase(unittest.TestCase):
    '''
    '''
    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

    def test_01_test_get_statuses(self):
        statuses = get_statuses('a', 1, 'b', 'c')
        self.assertEqual(statuses, EXPECTED_STATUSES)

    def test_02_test_add_to_db(self):
        add_to_db([{'id': 12345, 'created_at': 'Thu Aug 29 13:05:24 +0000 2019',
                    'text': 'lorem ipsum'}], 'news')
        tweet = Tweet.objects().first()
        self.assertEqual(tweet.tweet_id, 12345)

    def test_03_runner_no_tweet_query(self):
        sys.exit = MagicMock()
        runner(database='mongoenginetest', database_host='mongomock://localhost', oneshot=True)

    def tearDown(self):
        disconnect()

if __name__ == '__main__':
    classes = [WorkerTestCase]
    mytestrunner(classes)
