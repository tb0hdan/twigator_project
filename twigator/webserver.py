#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twigator web server module
"""

import os
from typing import Any, Collection

from apispec import APISpec  # type: ignore

from starlette.applications import Starlette
from starlette.responses import Response, UJSONResponse
from starlette_apispec import APISpecSchemaGenerator  # type: ignore

import sys
sys.path.insert(1, '..')
sys.path.insert(2, '.')

from twigator.db.connection import MongoConnection
from twigator.db.aggregations import get_tweet_count, get_top_hashtags, get_top_twitters
from twigator.db.queries import get_last_tweets, get_tweet_by_id, get_author_by_id


SCHEMAS = APISpecSchemaGenerator(
    APISpec(
        title="Tweet query API",
        version="1.0",
        openapi_version="3.0.0",
        info={"description": "Aggregate tweets and provide RESTful access to DB"},
    )
)

APP = Starlette(debug=True)


class ResponseBuilder:
    """
    Starlette Response builder.
    Uses UJSONResponse underneath.
    """
    def __init__(self) -> None:
        self.__response: dict = {}

    @property
    def response(self) -> dict:
        """
        Provide access to private __response attribute
        :return: dictionary containing response
        """
        return self.__response

    @property
    def json(self) -> UJSONResponse:
        """
        Build response from dictionary using fast converter

        :return: UJSONResponse object (usable inside app only)
        """
        return UJSONResponse(self.response)

    def set_status(self, status: str) -> None:
        """
        Set response status within JSON field

        :param status: one of the ['ok', 'error']
        :return:
        """
        self.__response['status'] = status

    def set_ok_status(self) -> None:
        """
        Wrapper around set_status (set to 'ok')
        :return: None
        """
        self.set_status('ok')

    def set_error_status(self) -> None:
        """
        Wrapper around set_status (set to 'error')
        :return: None
        """
        self.set_status('error')

    def set_result(self, result: Collection[Any]) -> None:
        """
        Provide a way to set private dictionary

        :param result: Dictionary that will be rendered as a JSON
        :return: None
        """
        self.__response['result'] = result


@APP.route("/", methods=["GET"])
async def homepage(_) -> UJSONResponse:
    """
    responses:
      200:
        description: A hello world response
        examples:
          { status: "ok", result: { hello: "world" }}
    """
    response = ResponseBuilder()
    response.set_ok_status()
    response.set_result({'hello': 'world'})
    return response.json


@APP.route("/tweets/{phrase:str}", methods=["GET"])
async def tweets(request) -> UJSONResponse:
    """
    responses:
      200:
        description: A hello world response
        examples:
          { status: "ok", result: { hello: "world" }}
    """
    limit: int = int(request.query_params.get('limit', 25))
    offset: int = int(request.query_params.get('offset', 0))
    response = ResponseBuilder()
    response.set_error_status()
    with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                         int(os.environ.get('MONGO_PORT', 27017))):
        query = request.path_params['phrase']
        query = '' if query in ['\"\"', '\'\''] else query
        result = get_last_tweets(query, limit=limit, offset=offset)
        response.set_ok_status()
    response.set_result(result)
    return response.json


@APP.route("/tweet/{tweet_id:int}", methods=["GET"])
async def tweet_by_id(request) -> UJSONResponse:
    """
    responses:
      200:
        description: A hello world response
        examples:
          { status: "ok", result: { hello: "world" }}
    """
    tweet_id: int = request.path_params['tweet_id']
    response = ResponseBuilder()
    if tweet_id < 0:
        response.set_error_status()
        return response.json
    with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                         int(os.environ.get('MONGO_PORT', 27017))):
        result = get_tweet_by_id(tweet_id)
        response.set_result(result)
    return response.json


@APP.route("/author/{author_id:int}", methods=["GET"])
async def author_by_id(request) -> UJSONResponse:
    """
    responses:
      200:
        description: A hello world response
        examples:
          { status: "ok", result: { hello: "world" }}
    """
    author_id: int = request.path_params['author_id']
    response = ResponseBuilder()
    if author_id < 0:
        response.set_error_status()
        return response.json
    with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                         int(os.environ.get('MONGO_PORT', 27017))):
        result = get_author_by_id(author_id)
        response.set_result(result)
    return response.json


@APP.route('/aggregation/{aggregation_name:str}/{query:str}', methods=["GET"])
async def aggregation(request) -> UJSONResponse:
    """
    responses:
      200:
        description: A hello world response
        examples:
          { status: "ok", result: { hello: "world" }}
    """
    result = ''
    status = 'error'
    query = request.path_params['query']
    query = '' if query in ['\"\"', '\'\''] else query
    print('`%s`' % query)
    aggregation_name = request.path_params['aggregation_name']
    if not aggregation_name in ['top_tags', 'tweet_count', 'top_twitters']:
        return UJSONResponse({'aggregation': aggregation_name, 'result': result, 'status': status})
    if aggregation_name == 'top_tags':
        with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                             int(os.environ.get('MONGO_PORT', 27017))):
            result = str(get_top_hashtags(query=query, limit=int(request.query_params.get('limit', 10))))
            status = 'ok'
    if aggregation_name == 'tweet_count':
        with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                             int(os.environ.get('MONGO_PORT', 27017))):
            result = str(get_tweet_count(query=query))
            status = 'ok'
    if aggregation_name == 'top_twitters':
        with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'),
                             int(os.environ.get('MONGO_PORT', 27017))):
            result = str(get_top_twitters(query=query, limit=int(request.query_params.get('limit', 10))))
            status = 'ok'
    return UJSONResponse({'aggregation': aggregation_name, 'result': result, 'status': status})


@APP.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request) -> Response:
    """
    Build OpenAPI schema and make it available at /schema
    :param request:
    :return:
    """
    return SCHEMAS.OpenAPIResponse(request=request)
