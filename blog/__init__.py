from os.path import dirname, join

from flask import Flask

from . import db


app = Flask(__name__)

# use sqlite database
# use from_mapping for configuration data and settings shareable across the app
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="sqlite:///" + join(dirname(dirname(__file__)), "database.sqlite"),
)

# initialize Flask-SQLAlchemy properly
db.init_app(app)

@app.route("/")
def index():
    return "Hello, World!"
