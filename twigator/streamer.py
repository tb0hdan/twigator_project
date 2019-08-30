#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter stream consumer module
"""

import sys
import threading
import time
import concurrent.futures

from queue import Queue


# 3rd
from twython import TwythonStreamer

sys.path.insert(1, '.')
sys.path.insert(2, '..')

from twigator.db.connection import MongoConnection  # pylint:disable=wrong-import-position
from twigator.worker import add_to_db  # pylint:disable=wrong-import-position
from twigator.envconfig import EnvConfig  # pylint:disable=wrong-import-position
from twigator.log import logger  # pylint:disable=wrong-import-position


class MyStreamer(TwythonStreamer):
    """
    Streamer subclass
    """
    def __init__(self, *args, **kwargs):
        super(MyStreamer, self).__init__(*args, **kwargs)
        self.track_query = ''
        self.queue = None

    def on_success(self, data):
        """
        Get tweet and put it into queue quickly

        :param data:
        :return:
        """
        if data.get('limit'):
            logger.debug('Got limit...')
            return
        self.queue.put_nowait(data)

    def on_error(self, status_code, data):
        """
        Disconnect on errors, including authentication, network etc

        :param status_code:
        :param data:
        :return:
        """
        logger.error('on_error: %d %s', status_code, data)
        self.disconnect()


class QueueReader:
    """
    Queue reader - get messages from queue and store them in database
    FIXME: Add autoscaling for MongoDB connections
    """
    def __init__(self, queue, query):
        self.queue = queue
        self.query = query
        self.exit = False

    def add_to_db(self, data):
        """
        Store tweet in database

        :param data:
        :return:
        """
        with MongoConnection():
            add_to_db([data], self.query)

    def process_chunk(self, chunk):
        """
        Process group of tweets in parallel in a predictable manner

        :param chunk:
        :return:
        """
        # FIXME: Use autoscaling
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            for post in chunk:
                executor.submit(self.add_to_db, post)

    def set_exit(self):
        """
        Request queue reader thread exit

        :return:
        """
        self.exit = True

    def run(self):
        """
        Actual queue reader runner

        :return:
        """
        chunk = []
        while not self.exit:
            if not self.queue.empty():
                # FIXME: Use autoscaling
                if len(chunk) < 32:
                    chunk.append(self.queue.get())
                else:
                    self.process_chunk(chunk)
                    chunk = [self.queue.get()]
                logger.debug('Queue size: %d', self.queue.qsize())
            else:
                time.sleep(0.01)


def run_streamer(query=None):
    """
    Configure both queue and MyStreamer and run processing

    :param query:
    :return:
    """
    queue = Queue()
    env_config = EnvConfig()
    query = query if query else env_config.TWEET_QUERY
    stream = MyStreamer(env_config.TWITTER_CONSUMER_KEY,
                        env_config.TWITTER_CONSUMER_SECRET,
                        env_config.TWITTER_OAUTH_KEY,
                        env_config.TWITTER_OAUTH_SECRET)
    stream.track_query = query
    stream.queue = queue
    #
    reader = QueueReader(queue, query)
    thread = threading.Thread(target=reader.run)
    thread.start()
    #
    try:
        stream.statuses.filter(track=query)
    except KeyboardInterrupt:
        reader.set_exit()
        thread.join()


if __name__ == '__main__':
    run_streamer()
