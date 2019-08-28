#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" OpenAPI schema builder"""

# std
import sys
import yaml


# project imports
sys.path.insert(1, '.')
from twigator.webserver import APP, SCHEMAS

if __name__ == '__main__':
    SCHEMA = SCHEMAS.get_schema(routes=APP.routes)
    print(yaml.dump(SCHEMA, default_flow_style=False))
