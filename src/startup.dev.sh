#!/bin/bash

apt-get install -y zip
pip3 install -r requirements.txt
chmod +x wait-for-it.sh
./wait-for-it.sh db:5432 --timeout=0
python3 api.py