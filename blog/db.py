# blog/db.py - code related to the database

from datetime import datetime

from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext


# Initialize the Flask-SQLAlchemy extension with no settings/configs
# db global object for creating database models
# and managing relationships with the database.
db = SQLAlchemy()


class Post(db.Model):
    """A blog post."""

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)


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
