from typing import Any, Dict, List, Optional

from .entities import Tweet


def get_top_hashtags(query: Optional[str] = None, limit: Optional[int] = 10) -> List[Any]:
    """
    """
    pipeline: List[Dict[Any, Any]] = [{"$match": {"$text": {"$search": query}}}] if query else []
    pipeline += [{"$unwind": "$hashtags"},
                 {"$group": {"_id": "$hashtags", "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": limit},
    ]
    return [x for x in Tweet.objects.aggregate(*pipeline)]


def get_tweet_count(query: Optional[str] = None) -> int:
    """
    """
    pipeline: List[Dict[Any, Any]] = [{"$match": {"$text": {"$search": query}}}] if query else []
    pipeline += [{"$count": "postcnt"},
               ]
    response = [x for x in Tweet.objects.aggregate(*pipeline)]
    return response[0].get('postcnt') if len(response) == 1 else 0


def get_top_twitters(query: Optional[str] = None, limit: Optional[int] = 3) -> List[Any]:
    """
    """
    pipeline: List[Dict[Any, Any]] = [{"$match": {"$text": {"$search": query}}}] if query else []
    pipeline += [
                 {"$group": {"_id": "$author_id", "postcnt": {"$sum": 1}}},
                 {"$sort": {"postcnt": -1}},
                 {"$limit": limit},
               ]
    return [x for x in Tweet.objects.aggregate(*pipeline)]
