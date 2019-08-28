from operator import itemgetter
from .entities import Tweet


def get_top_hashtags(query=None, limit=10):
    """
    """
    pipeline = [{ "$match": {"$text":{"$search":query}}}] if query else []
    pipeline += [{ "$unwind": "$hashtags" },
                 { "$group": { "_id": "$hashtags", "count": { "$sum": 1 }}},
                 { "$sort": {"count": -1}},
                 { "$limit": 3},
    ]
    return [x for x in Tweet.objects.aggregate(*pipeline)]


def get_tweet_count(query=None):
    """
    """
    pipeline = [{ "$match": {"$text":{"$search":query}}}] if query else []
    pipeline +=  [{ "$count": "postcnt"},
               ]
    response = [x for x in Tweet.objects.aggregate(*pipeline)]
    return response[0].get('postcnt') if len(response) == 1 else 0


def get_top_twitters(query=None, limit=3):
    """
    """
    pipeline = [{ "$match": {"$text":{"$search":query}}}] if query else []
    pipeline += [
                 { "$group": { "_id": "$author_id", "postcnt": { "$sum": 1 }}},
                 { "$sort": {"postcnt": -1 }},
                 { "$limit": limit },
               ]
    return [x for x in Tweet.objects.aggregate(*pipeline)]
