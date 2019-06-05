# blog/auth.py - Login and Logout views

from os import environ

from flask import Blueprint, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient


# Blueprints help to modularize code and make it reusable in large systems.
# Each has a name, a URL prefix, and it’s own mini application object.
bp = Blueprint("auth", __name__, url_prefix="/")
oidc = OpenIDConnect()
OKTA_AUTH_TOKEN = environ.get(
    'OKTA_AUTH_TOKEN', "00aYeDir7eOx_xuUuaNTpPzH1ox3UKS_Etcq-vNkMI")

# Allows retrieval of user data from the Okta API
okta_client = UsersClient("https://dev-312288.okta.com", OKTA_AUTH_TOKEN)


@bp.route("/login")
@oidc.require_login
def login():
    """
    Force the user login and redirect to user dashboard.

    If logged in (@oidc.require_login), redirect to dashboard.
    Otherwise, redirect to Okta authorization server and prompt user registration,
    or logging into an existing account.
    """

    return redirect(url_for("blog.dashboard"))


@bp.route("/logout")
def logout():
    """
    Logs user out of their account.

    Delete the session cookie (via the oidc.logout() call),
    and redirect to the homepage
    """

    oidc.logout()
    return redirect(url_for("blog.index"))
