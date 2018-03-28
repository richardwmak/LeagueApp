r"""
Controller.
"""
import logging
from time import time
from typing import Any

from flask import Blueprint, redirect, request, url_for, render_template
from model.auth import Auth
from model.api import ApiRequest
from model.custom_session import Session
from view.login import login_render
from view.stats import stats_render

# Set up logging.
logger = logging.getLogger(__name__)

# Set up Flask blueprint
MAIN_APP = Blueprint("MAIN_APP", __name__)

# initialise session
SESSION = Session()

logger.info("Loaded session.")

# Create data object to use this session
API = ApiRequest()
AUTH = Auth()

# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@MAIN_APP.route("/")
def main_page(session: Session = SESSION) -> Any:
    """Route to login or main screen."""
    if session.check_key("listen_history.done") and session.select_key(
            "listen_history.done") == 1:
        return redirect(url_for("MAIN_APP.stats"))
    elif session.check_key("logged_in") and session.select_key("logged_in"):
        return redirect(url_for("MAIN_APP.get_info"))
    else:
        return redirect(url_for("MAIN_APP.login"))


@MAIN_APP.route("/login")
def login(auth: Auth = AUTH) -> Any:
    """Request user info."""
    auth_url = auth.generate_auth_url()
    return login_render(auth_url=auth_url)


@MAIN_APP.route("/set_info", methods=["GET"])
def set_info(auth: Auth = AUTH) -> Any:
    """Get the token obtained from authorisation, then get the session key.

    Keyword Arguments:
        api {ApiRequest} -- (default: {API})
    """
    # set the token
    new_token = request.args.get("token")
    auth.get_session_key(new_token, API, SESSION)
    # TODO: pretty sure this won't do anything if it fails...
    return redirect(url_for("MAIN_APP.get_info"))


@MAIN_APP.route("/get_info")
def get_info() -> Any:
    """Load the page that displays while user info is getting fetched.
    """
    return render_template("get_info.html", timestamp=time())


@MAIN_APP.route("/stats")
def stats() -> Any:
    """Load main page."""
    return stats_render()
