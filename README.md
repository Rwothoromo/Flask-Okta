# Flask-Okta

A simple Flask CRUD application with secure [Okta authentication](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python).

## Requirements

* Install [Python 3](https://www.python.org/downloads/).
* Run pip install virtualenv on command prompt

## Setup

* Run `git clone https://github.com/Rwothoromo/Flask-Okta.git` and `cd` into the project root.
* Run `virtualenv ../flask-okta-venv --python=python3` for Mac/Linux.
* Run `source ../flask-okta-venv/bin/activate` for Mac/Linux.
* Run `pip install -r requirements.txt`.
* Run `FLASK_APP=blog flask init-db` to initialize an sqlite database.
* Run `FLASK_APP=blog flask run` to start the app.
