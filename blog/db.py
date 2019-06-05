# blog/db.py - code related to the database

from datetime import datetime

from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext


# Initialize the Flask-SQLAlchemy extension with no settings/configs
# db global object for creating database models
# and managing relationships with the database.
db = SQLAlchemy()


@command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""

    db.create_all()
    echo("Initialized the database.")


def init_app(app):
    """Initialize the Flask app for database usage."""

    db.init_app(app)
    # Allow usage of the cli command `FLASK_APP=blog flask init-db`
    app.cli.add_command(init_db_command)
