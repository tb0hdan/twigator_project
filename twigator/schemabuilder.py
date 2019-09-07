#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" OpenAPI schema builder"""

# std
import sys
import yaml

from typing import Union

# project imports
sys.path.insert(1, '.')
from twigator.webserver import APP, SCHEMAS

def get_schema() -> Union[str, bytes]:
    SCHEMA = SCHEMAS.get_schema(routes=APP.routes)
    return yaml.dump(SCHEMA, default_flow_style=False)

if __name__ == '__main__':
    print(get_schema())
