from os import environ

# third party imports
from flask import Flask, g, render_template
from flask_cors import CORS

# local imports
from config import app_config, configure_app
from blog.db import db
from blog.cache import cache
from blog.admin.controllers import admin
from blog.auth.controllers import auth, oidc
from blog.main.controllers import main


def create_app():
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)

    configuration = environ.get('FLASK_ENV', 'production')
    app.config.from_object(app_config[configuration])

    oidc.init_app(app)
    db.init_app(app)

    # Handle Cross Origin Resource Sharing, making cross-origin AJAX possible
    # Allows a web application running at one origin (domain)
    # to access selected resources from a server at a different origin
    CORS(app)

    # Configure Compressing
    configure_app(app)

    # Lazy initialization
    cache.init_app(app)

    # apply the blueprints to the app
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(auth)
    app.register_blueprint(main, url_prefix='/')
    return app


app = create_app()


@app.before_request
def before_request():
    """
    Load a user object into `g.user` before each request.
    """

    # Check whether or not the server-side cookie (session created on log in) exists and is valid

    g.user = auth.okta_client.get_user(oidc.user_getfield(
        "sub")) if oidc.user_loggedin else None


@app.errorhandler(404)
def page_not_found(e):
    """Render 404 page."""

    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def unauthorized_access(e):
    """Render 403 page."""

    return render_template("errors/403.html"), 403
