#!/usr/bin/env python3

import os

import uvicorn
from apispec import APISpec

from starlette.applications import Starlette
from starlette.responses import UJSONResponse
from starlette_apispec import APISpecSchemaGenerator

import sys
sys.path.insert(1, '..')
sys.path.insert(2, '.')

from twigator.db.connection import MongoConnection
from twigator.db.aggregations import get_tweet_count, get_top_hashtags
from twigator.log import logger

schemas = APISpecSchemaGenerator(
    APISpec(
        title="Tweet query API",
        version="1.0",
        openapi_version="3.0.0",
        info={"description": "explanation of the api purpose"},
    )
)

app = Starlette(debug=True)

@app.route("/", methods=["GET"])
async def homepage(request):
    """
    responses:
      200:
        description: A list of users.
        examples:
          [{"username": "tom"}, {"username": "lucy"}]
    """
    return UJSONResponse({'hello': 'world'})

@app.route('/aggregation/{aggregation_name:str}', methods=["GET"])
async def aggregation(request):
    """
    """
    result = ''
    status = 'error'
    aggregation_name = request.path_params['aggregation_name']
    if not aggregation_name in ['top_tags', 'tweet_count']:
        return UJSONResponse({'aggregation': aggregation_name, 'result': result, 'status': status})
    if aggregation_name == 'top_tags':
        with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'), int(os.environ.get('MONGO_PORT', 27017))):
            result = get_top_hashtags(limit=int(request.query_params.get('limit', 10)))
            status = 'ok'
    if aggregation_name == 'tweet_count':
        with MongoConnection('twitter', os.environ.get('MONGO_HOST', 'localhost'), int(os.environ.get('MONGO_PORT', 27017))):
            result = get_tweet_count()
            status = 'ok'
    return UJSONResponse({'aggregation': aggregation_name, 'result': result, 'status': status})


@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


if __name__ == '__main__':
    import sys
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run(app, host='0.0.0.0', port=8000)
    elif sys.argv[-1] == "schema":
        schema = schemas.get_schema(routes=app.routes)
        import yaml
        logger.warning(yaml.dump(schema, default_flow_style=False))
