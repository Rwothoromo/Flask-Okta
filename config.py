from os import environ
from os.path import join, dirname


class Config:
    """
    Common configurations
    """

    # private variable to secure the Flask sessions (cookies) from tampering
    SECRET_KEY = environ.get(
        'SECRET_KEY', 'djgddgdkbgdihbfhfhrurwowruu384573wrpe2dwjd2bh@##$FSHF')

    # use sqlite database
    SQLALCHEMY_DATABASE_URI = environ.get(
        'SQLALCHEMY_DATABASE_URI', "sqlite:///" + join(dirname(__file__), "database.sqlite"))

    # get the root url and concantenate it with the client secrets file
    OIDC_CLIENT_SECRETS = join(dirname(__file__), "client_secrets.json")

    # test out login and registration in development without using SSL
    OIDC_COOKIE_SECURE = False

    # URL to handle user login
    OIDC_CALLBACK_ROUTE = "/oidc/callback"

    # what user data to request on log in
    OIDC_SCOPES = ["openid", "email", "profile"]

    OIDC_ID_TOKEN_COOKIE_NAME = "oidc_token"

    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True  # protect against CSRF attacks
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
