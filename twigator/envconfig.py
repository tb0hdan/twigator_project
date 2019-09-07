#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration based on environment
"""
import os
import string

ENV_DEFAULTS = {'MONGO_DATABASE': 'twitter',
                'MONGO_HOST': 'localhost',
                'MONGO_PORT': 27017,
                'TWEET_LAST_TWEETS': 10,
                'TWEET_EVERY_MINUTES': 1,
                'TWEET_QUERY': 'news',
                'TWITTER_CONSUMER_KEY': '',
                'TWITTER_CONSUMER_SECRET': ''}

class EnvConfig:
    """
    Configure variables using os.environ or defaults
    """
    def __init__(self, defaults=None, environment=None):
        self.environment = environment if environment else os.environ
        self.defaults = defaults if defaults else ENV_DEFAULTS

    @staticmethod
    def check_var(var: str) -> bool:
        """
        Confirm that requested attribute is ALL CAPITAL (plus underscore)
        :param var:
        :return:
        """
        return all([x in string.digits + string.ascii_uppercase + '_' for x in var])

    def __getattr__(self, attr):
        """
        Check for attribute in os.environ, then in defaults, then fail :-)

        :param attr: Requested attribute
        :return: Attribute value
        """
        if not self.check_var(attr):
            raise AttributeError
        if self.environment.get(attr):
            return self.environment.get(attr)
        if self.defaults.get(attr) is not None:
            return self.defaults.get(attr)
        raise AttributeError
