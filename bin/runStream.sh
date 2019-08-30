#!/bin/bash

export MONGO_HOST=${MONGO_HOST:-localhost}
export MONGO_PORT=${MONGO_PORT:-27017}
export TWEET_QUERY=${TWEET_QUERY:-"twitter"}
export TWITTER_CONSUMER_KEY=${TWITTER_CONSUMER_KEY:-""}
export TWITTER_CONSUMER_SECRET=${TWITTER_CONSUMER_SECRET:-""}
export TWITTER_OAUTH_KEY=${TWITTER_OAUTH_KEY:-""}
export TWITTER_OAUTH_SECRET=${TWITTER_OAUTH_SECRET:-""}

cd $(dirname $0)/../twigator
python3 ./streamer.py
