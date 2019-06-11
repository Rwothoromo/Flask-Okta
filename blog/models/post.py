from datetime import datetime

from blog.db import db


class Post(db.Model):
    """A blog post."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False, unique=True)
