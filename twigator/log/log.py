# -*- coding: utf-8 -*-
"""
Logger module
"""
import logging

logger = logging.getLogger()  #pylint:disable=invalid-name
logger.setLevel(logging.DEBUG)
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
logger.addHandler(HANDLER)
