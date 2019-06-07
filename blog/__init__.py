from os import environ

# third party imports
from flask import Flask, g, render_template
from flask_cors import CORS

# local imports
from blog.db import db
from .views import auth, blog
from config import app_config


def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    configuration = environ.get('FLASK_ENV', 'production')
    app.config.from_object(app_config[configuration])

    auth.oidc.init_app(app)
    db.init_app(app)
    cors = CORS(app)

    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    return app


app = create_app()


@app.before_request
def before_request():
    """
    Load a user object into `g.user` before each request.
    """

    # Check whether or not the server-side cookie (session created on log in) exists and is valid

    g.user = auth.okta_client.get_user(auth.oidc.user_getfield(
        "sub")) if auth.oidc.user_loggedin else None


@app.errorhandler(404)
def page_not_found(e):
    """Render 404 page."""

    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def unauthorized_access(e):
    """Render 403 page."""

    return render_template("errors/403.html"), 403
