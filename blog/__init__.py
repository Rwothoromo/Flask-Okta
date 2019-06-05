import os

from flask import Flask, g

from . import auth, db


app = Flask(__name__)

# use sqlite database
# use from_mapping for configuration data and settings shareable across the app
app.config.from_mapping(
    # private variable to secure the Flask sessions (cookies) from tampering
    SECRET_KEY=os.environ.get(
        'SECRET_KEY', 'djgddgdkbgdihbfhfhrurwowruu384573wrpe2dwjd2bh@##$FSHF'),

    OIDC_CLIENT_SECRETS=join(os.path.dirname(
        os.path.dirname(__file__)), "client_secrets.json"),

    # test out login and registration in development without using SSL
    OIDC_COOKIE_SECURE=False,

    # URL to handle user login
    OIDC_CALLBACK_ROUTE="/oidc/callback",

    # what user data to request on log in
    OIDC_SCOPES=["openid", "email", "profile"],

    OIDC_ID_TOKEN_COOKIE_NAME="oidc_token",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + \
    os.path.join(dirname(dirname(__file__)), "database.sqlite"),
)

# initialize Flask-SQLAlchemy properly
db.init_app(app)


app.register_blueprint(auth.bp)


@app.route("/")
def index():
    return "Hello, World!"


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
