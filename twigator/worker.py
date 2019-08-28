#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime
import os
import sys
import time

from twython import Twython

sys.path.insert(1, '..')
sys.path.insert(2, '.')

from twigator.db.entities import Tweet
from twigator.db.connection import MongoConnection
from twigator.log import logger
from twigator.envconfig import  EnvConfig


def get_statuses(query, tweet_count, consumer_key, consumer_secret):
    python_tweets = Twython(consumer_key, consumer_secret)
    query = {'q': query,
            #'result_type': 'popular',
            'count': tweet_count,
            #'lang': 'en',
            }
    return python_tweets.search(**query)['statuses']


def add_to_db(statuses, query_phrases):
    for status in statuses:
        tweet_id: int = status.get('id')
        matches = Tweet.objects(tweet_id=tweet_id)
        if matches:
            logger.warning('Existing tweet with id: %d' % tweet_id)
            continue
        # Got new tweet, save it
        format = "%a %b %d %H:%M:%S %z %Y"
        published_at = datetime.datetime.strptime(status.get('created_at'), format)
        phrase = status.get('text')
        hashtags = [x.get('text', '') for x in status.get('entities', {}).get('hashtags', [])]
        author_id = status.get('user', {}).get('id', 0)
        tweet = Tweet(tweet_id=tweet_id, published_at=published_at,
                      phrase=phrase, hashtags=hashtags, author_id=author_id,
                      query_phrases=[x.strip() for x in query_phrases.split(',')])
        tweet.save()
    return


def runner(tweet_count=None, tweet_schedule=None, tweet_query=None,
           consumer_key=None, consumer_secret=None):
    """
    Run aggregation
    :param tweet_count:
    :param tweet_schedule:
    :param tweet_query:
    :param consumer_key:
    :param consumer_secret:
    :return:
    """
    env_config = EnvConfig()
    tweet_count: int = tweet_count if tweet_count else int(env_config.TWEET_LAST_TWEETS)
    tweet_schedule: int = tweet_schedule if tweet_schedule else int(env_config.TWEET_EVERY_MINUTES)
    tweet_query: str = tweet_query if tweet_query else env_config.TWEET_QUERY
    consumer_key: str = consumer_key if consumer_key else env_config.TWITTER_CONSUMER_KEY
    consumer_secret: str = consumer_secret if consumer_secret else env_config.TWITTER_CONSUMER_SECRET

    if not tweet_query:
        logger.error('Cannot run with empty query...')
        sys.exit(127)

    if not consumer_key or not consumer_secret:
        logger.error('Cannot run without auth...')
        sys.exit(129)
    logger.info('Getting %d tweets every %d minute(s)' % (tweet_count, tweet_schedule))
    while True:
        # Run!
        statuses = get_statuses(tweet_query, tweet_count, consumer_key, consumer_secret)
        logger.info('Status length: %d', len(statuses))
        with MongoConnection():
            add_to_db(statuses, tweet_query)
        logger.info('Sleeping for %d minute(s) until next fetch...', tweet_schedule)
        try:
            time.sleep(tweet_schedule * 60)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    runner()
