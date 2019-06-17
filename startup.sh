#! /bin/bash
# Sets up env variables and runs app
sudo su -
cd Flask-Okta
virtualenv ../flask-okta-venv --python=python3
source .env
python manage.py runserver
