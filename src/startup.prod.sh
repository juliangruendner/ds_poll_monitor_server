#!/bin/bash
apt-get install -y zip
uwsgi --ini uwsgi.ini
# python3 api.py