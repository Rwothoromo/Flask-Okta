#! /bin/bash
# Sets up env variables and database
sudo su -
sudo apt update
sudo apt install python3-pip
pip3 install virtualenv
cd Flask-Okta
virtualenv ../flask-okta-venv --python=python3
pip install -r requirements.txt
source .env
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
