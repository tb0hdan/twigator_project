#!/bin/bash

export TWEET_LAST_TWEETS=${TWEET_LAST_TWEETS:-100}
export TWEET_EVERY_MINUTES=${TWEET_EVERY_MINUTES:-1}
export TWEET_QUERY=${TWEET_QUERY:-"twitter"}
export MONGO_HOST=${MONGO_HOST:-localhost}
export MONGO_PORT=${MONGO_PORT:-27017}

cd $(dirname $0)/../twigator
python3 ./worker.py
