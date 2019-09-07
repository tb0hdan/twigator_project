twigator project - twitter aggregator project
=======


[![Build Status](https://api.travis-ci.org/tb0hdan/twigator_project.svg?branch=master)](https://travis-ci.org/tb0hdan/twigator_project)
[![Code Climate](https://codeclimate.com/github/tb0hdan/twigator_project/badges/gpa.svg)](https://codeclimate.com/github/tb0hdan/twigator_project)
[![Test Coverage](https://codeclimate.com/github/tb0hdan/twigator_project/badges/coverage.svg)](https://codeclimate.com/github/tb0hdan/twigator_project/coverage)
[![Issue Count](https://codeclimate.com/github/tb0hdan/twigator_project/badges/issue_count.svg)](https://codeclimate.com/github/tb0hdan/twigator_project)

- [DESCRIPTION](#description)
- [PRIVACY NOTICE](#privacy-notice)
- [INSTALLATION](#installation)
- [CONFIGURATION](#configuration)
- [USAGE](#usage)
- [ENDPOINTS](#endpoints)
- [DEVELOPMENT](#development)

## Description
Twigator project is a twitter message aggregator that searches messages periodically (using Twitter Search API)
stores them in database (MongoDB) and exposes RESTFul API for queries.

## Privacy notice
This project is created purely for educational purposes as a hands-on exercise using Twython, MongoEngine 
and MongoDB aggregations. Please respect privacy of the others if you're going to use it.

## Installation
This project requires Docker, Docker Compose and make for most use cases.

## Configuration
Configuration is done via environment variables on host system. The list is as follows:
- TWITTER_CONSUMER_KEY
- TWITTER_CONSUMER_SECRET
- TWEET_LAST_TWEETS - amount of new tweets to ingest
- TWEET_EVERY_MINUTES - parse tweets every X minutes (at least 1)
- TWEET_QUERY - search criteria

## Usage
To get familiar with the project, start by typing: `make`
After few moments HTTP API will be available at http://localhost:8000

To stop containers, type: `make stop`

### Endpoints
To get all values for URLs with queries provide "" or '' as query, e.g.

`http://localhost:8000/tweets/''`

Queries:

- http://localhost:8000/author/author_id
- http://localhost:8000/tweet/tweet_id
- http://localhost:8000/tweets/query

Aggregations:

- http://localhost:8000/aggregation/top_tags/query
- http://localhost:8000/aggregation/top_twitters/query
- http://localhost:8000/aggregation/tweet_count/query

## Development

### Running tests

Following test group are ran every time `tests`
target is requested:

- PyLint
- MyPy
- Unit tests
- Unit tests + Coverage

Command to run all test groups:

`make tests`

### API documentation

API documentation is available after running `make` at:

- http://localhost:8000/swagger
