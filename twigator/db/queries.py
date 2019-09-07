import datetime
import json

from typing import Any, Collection, Optional
from .entities import Tweet


DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


def tweet_to_dict(tweet: Tweet) -> dict:
    # do partial conversion
    parsed_tweet = json.loads(tweet.to_json())
    del parsed_tweet['_id']
    del parsed_tweet['published_at']
    del parsed_tweet['tweet_id']
    parsed_tweet['published_at'] = tweet.published_at.strftime(DATE_FORMAT)
    # Nasty hack for broken JSON Viewers (such as Google Chrome)
    # Works just fine in Safari
    parsed_tweet['tweet_id'] = str(tweet.tweet_id)
    return parsed_tweet


def get_last_tweets(phrase: Optional[str] = '',
                    limit: int = 10,
                    offset: int = 0,
                    date_after: Optional[str] = None):
    """
    """
    if offset > limit:
        offset = limit
    response = []
    query = {'phrase__contains': phrase}
    if date_after:
        after = datetime.datetime.strptime(date_after, DATE_FORMAT)
        query['published_at__gte'] = str(after)
    tweets = Tweet.objects(**query).order_by('-published_at')[offset:limit]
    for tweet in tweets:
        response.append(tweet_to_dict(tweet))
    return response


def get_tweet_by_id(tweet_id: int) -> Collection[Any]:
    objects = Tweet.objects(tweet_id=tweet_id)
    response = [x for x in objects]
    return tweet_to_dict(response[0]) if len(objects) == 1 else []


def get_author_by_id(author_id: int,
                     limit: int = 10,
                     offset: int = 0):
    response = []
    if offset > limit:
        offset = limit
    tweets = Tweet.objects(author_id=author_id).order_by('-published_at')[offset:limit]
    for tweet in tweets:
        response.append(tweet_to_dict(tweet))
    return response
