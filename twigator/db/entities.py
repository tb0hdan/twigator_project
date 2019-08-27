# -*- coding: utf-8 -*-
"""
Twitter parser database module
"""

import datetime
from mongoengine import Document, DateTimeField, StringField, ListField, LongField

class Tweet(Document):
    """
    id: 852021818290352129
    published_at: 2017-04-12 04:53:25
    phrase: Watch NASA's first 4K broadcast from space on April 26th - ...
    hashtags: NASA, space, broadcast
    author_id: 622857704
    query_phrases: NASA broadcast, NASA 4K
    """
    tweet_id = LongField(required=True)
    published_at = DateTimeField(default=datetime.datetime.utcnow, required=True)
    phrase = StringField(required=True)
    hashtags = ListField(StringField())  # can be empty
    author_id = LongField(required=True)
    query_phrases = ListField(StringField(), required=True)
