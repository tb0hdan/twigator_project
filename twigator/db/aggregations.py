from operator import itemgetter
from .entities import Tweet

# aggregations
def get_top_hashtags(limit=10):
    hashtag_freqs = Tweet.objects.item_frequencies('hashtags', normalize=True)
    top_tags = sorted(hashtag_freqs.items(), key=itemgetter(1), reverse=True)[:limit]
    return top_tags

def get_tweet_count():
    return Tweet.objects.count()
