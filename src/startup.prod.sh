apt-get install -y zip
pip3 install -r requirements.txt
uwsgi --ini uwsgi.ini
# python3 api.py