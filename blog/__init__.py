from os import environ
from os.path import dirname, join

from flask import Flask, g, render_template

from . import auth, blog, db


app = Flask(__name__)

# use from_mapping for configuration data and settings shareable across the app
app.config.from_mapping(
    # private variable to secure the Flask sessions (cookies) from tampering
    SECRET_KEY=environ.get(
        'SECRET_KEY', 'djgddgdkbgdihbfhfhrurwowruu384573wrpe2dwjd2bh@##$FSHF'),

    # get the root url and concantenate it with the client secrets file
    OIDC_CLIENT_SECRETS=join(
        dirname(dirname(__file__)), "client_secrets.json"),

    # test out login and registration in development without using SSL
    OIDC_COOKIE_SECURE=False,

    # URL to handle user login
    OIDC_CALLBACK_ROUTE="/oidc/callback",

    # what user data to request on log in
    OIDC_SCOPES=["openid", "email", "profile"],

    OIDC_ID_TOKEN_COOKIE_NAME="oidc_token",

    # use sqlite database
    SQLALCHEMY_DATABASE_URI="sqlite:///" + \
    join(dirname(dirname(__file__)), "database.sqlite"),
)

auth.oidc.init_app(app)

# initialize Flask-SQLAlchemy properly
db.init_app(app)


app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)


@app.before_request
def before_request():
    """
    Load a user object into `g.user` before each request.
    """

    # Check whether or not the server-side cookie (session created on log in) exists and is valid
    if auth.oidc.user_loggedin:
        g.user = auth.okta_client.get_user(auth.oidc.user_getfield("sub"))
    else:
        g.user = None


@app.errorhandler(404)
def page_not_found(e):
    """Render 404 page."""

    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def unauthorized_access(e):
    """Render 403 page."""

    return render_template("errors/403.html"), 403
