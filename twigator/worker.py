#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import datetime
import os
import sys
import threading
import time

from twython import Twython

import sys
sys.path.insert(1, '..')
sys.path.insert(2, '.')

from twigator.db.entities import Tweet
from twigator.db.connection import MongoConnection
from twigator.log import logger


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

if __name__ == '__main__':
    environment = os.environ
    tweet_count: int = int(environment.get('TWEET_LAST_TWEETS', 1))
    tweet_schedule: int = int(environment.get('TWEET_EVERY_MINUTES', 1))
    tweet_query: str = environment.get('TWEET_QUERY', '')
    if not tweet_query:
        logger.error('Cannot run with empty query...')
        sys.exit(127)
    consumer_key: str = environment.get('TWITTER_CONSUMER_KEY')
    consumer_secret: str = environment.get('TWITTER_CONSUMER_SECRET')
    if not consumer_key or not consumer_secret:
        logger.error('Cannot run without auth...')
        sys.exit(129)
    logger.info('Getting %d tweets every %d minute(s)' % (tweet_count, tweet_schedule))
    while True:
        # Run!
        statuses = get_statuses(tweet_query, tweet_count, consumer_key, consumer_secret)
        logger.info('Status length: %d', len(statuses))
        with MongoConnection('twitter', os.environ.get('MONGO_HOST'), int(os.environ.get('MONGO_PORT'))):
            add_to_db(statuses, tweet_query)
        logger.info('Sleeping for %d minute(s) until next fetch...', tweet_schedule)
        try:
            time.sleep(tweet_schedule * 60)
        except KeyboardInterrupt:
            break
