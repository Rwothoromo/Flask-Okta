#! /bin/bash
# Sets up env variables and database
sudo su -
pip install -r requirements.txt
source .env
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
