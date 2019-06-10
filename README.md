# Flask-Okta

A simple Flask CRUD application with secure [Okta authentication](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python).

## Requirements

- Install [Python 3](https://www.python.org/downloads/).
- Run `pip install virtualenv` on command prompt.

## First things first

- You need Okta, to store user accounts and provide easy authentication and authorization. Create an [Okta developer account](https://developer.okta.com/signup).
- In your Okta dev account, create an app (under `Applications`) of type `Web` and set the redirect uris to `http://localhost:5000/oidc/callback`.
- Also, get an API token under `API`.
- Be sure to enable self-registration on the `Classic UI` under `Directory`.
- Create a `client_secrets.json` file (with the details that follow) at the root of your project folder.

```json
{
  "web": {
    "client_id": "{{ OKTA_CLIENT_ID }}",
    "client_secret": "{{ OKTA_CLIENT_SECRET }}",
    "auth_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/authorize",
    "token_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/token",
    "issuer": "{{ OKTA_ORG_URL }}/oauth2/default",
    "userinfo_uri": "{{ OKTA_ORG_URL }}/oauth2/default/userinfo",
    "redirect_uris": [
      "http://localhost:5000"
    ]
  }
}
```

## Setup

- Run `git clone https://github.com/Rwothoromo/Flask-Okta.git` and `cd` into the project root.
- Run `virtualenv ../flask-okta-venv --python=python3` for Mac/Linux.
- Run `source ../flask-okta-venv/bin/activate` for Mac/Linux.
- Run `pip install -r requirements.txt`.
- Run `export SECRET_KEY=<some_secret_value>`.
- Run `export OKTA_AUTH_TOKEN=<okta_auth_token>`.
- Run `export OKTA_ORG_URL=<okta_org_url>`.
- Run `export SQLALCHEMY_DATABASE_URI=<path_to_sqlalchemy_database>`
- Run `export FLASK_ENV=development`
- Run `export FLASK_APP=blog`.
- Run the following to set up the database/migrations:
  - `python manage.py db init` to create a migration repository.
  - `python manage.py db migrate` to update the migration script.
  - `python manage.py db upgrade` to apply the migration to the database.
- Run `python manage.py runserver` to run on the default ip and port.
- View the app on `http://127.0.0.1:5000/`.
