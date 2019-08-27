#!/bin/bash

cd $(dirname $0)/../twigator
gunicorn -c ../etc/settings.py webserver:app

