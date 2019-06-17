#! /bin/bash
# Sets up env variables and runs app
sudo su -
cd /home/elijah_rwothoromo/Flask-Okta
source ../flask-okta-venv/bin/activate
source .env
python manage.py runserver
