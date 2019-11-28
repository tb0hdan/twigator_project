#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime
import sys
import time

from typing import List, Optional

import twython  # type: ignore

sys.path.insert(1, '..')
sys.path.insert(2, '.')

from twigator.db.entities import Tweet
from twigator.db.connection import MongoConnection
from twigator.log import logger
from twigator.envconfig import  EnvConfig


def get_statuses(in_query: str, tweet_count: int, consumer_key: str, consumer_secret: str) -> List[dict]:
    python_tweets = twython.Twython(consumer_key, consumer_secret)
    query = {'q': in_query,
            #'result_type': 'popular',
            'count': tweet_count,
            #'lang': 'en',
            }
    return python_tweets.search(**query)['statuses']


def add_to_db(statuses: List[dict], query_phrases: str) -> None:
    for status in statuses:
        tweet_id: int = int(status.get('id', 0))
        if not tweet_id:
            continue
        matches = Tweet.objects(tweet_id=tweet_id)
        if matches:
            logger.warning('Existing tweet with id: %d' % tweet_id)
            continue
        # Got new tweet, save it
        format = "%a %b %d %H:%M:%S %z %Y"
        published_at = datetime.datetime.strptime(str(status.get('created_at')), format)
        phrase = status.get('text')
        hashtags = [x.get('text', '') for x in status.get('entities', {}).get('hashtags', [])]
        author_id = status.get('user', {}).get('id', 0)
        tweet = Tweet(tweet_id=tweet_id, published_at=published_at,
                      phrase=phrase, hashtags=hashtags, author_id=author_id,
                      query_phrases=[x.strip() for x in query_phrases.split(',')])
        tweet.save()
    return


def runner(tweet_count: Optional[int] = None,
           tweet_schedule: Optional[int] = None,
           tweet_query: Optional[str] = None,
           consumer_key: Optional[str] = None,
           consumer_secret: Optional[str] = None,
           database: Optional[str] = None,
           database_host: Optional[str] = None,
           oneshot=False):
    """
    Run aggregation
    :param tweet_count:
    :param tweet_schedule:
    :param tweet_query:
    :param consumer_key:
    :param consumer_secret:
    :param database:
    :param database_host:
    :param oneshot:
    :return:
    """
    env_config = EnvConfig()
    tweet_count_: int = tweet_count if tweet_count else int(env_config.TWEET_LAST_TWEETS)
    tweet_schedule_: int = tweet_schedule if tweet_schedule else int(env_config.TWEET_EVERY_MINUTES)
    tweet_query_: str = tweet_query if tweet_query else env_config.TWEET_QUERY
    consumer_key_: str = consumer_key if consumer_key else env_config.TWITTER_CONSUMER_KEY
    consumer_secret_: str = consumer_secret if consumer_secret else env_config.TWITTER_CONSUMER_SECRET

    if not tweet_query_:
        logger.error('Cannot run with empty query...')
        sys.exit(127)

    if not consumer_key_ or not consumer_secret_:
        logger.error('Cannot run without auth...')
        sys.exit(129)
    logger.info('Getting %d tweets every %d minute(s)' % (tweet_count_, tweet_schedule_))
    while True:
        # Run!
        statuses = get_statuses(tweet_query_, tweet_count_, consumer_key_, consumer_secret_)
        logger.info('Status length: %d', len(statuses))
        with MongoConnection(db=database, host=database_host):
            add_to_db(statuses, tweet_query_)
        logger.info('Sleeping for %d minute(s) until next fetch...', tweet_schedule_)
        if oneshot:
            break
        try:
            time.sleep(tweet_schedule_ * 60)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    runner()
