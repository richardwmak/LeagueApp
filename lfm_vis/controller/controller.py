r"""
Controller.
"""
from   flask import Blueprint, redirect, request, url_for, render_template
import logging
import os
from   model.auth import Auth
from   model.api import ApiRequest
import model.custom_session as custom_session
import sys
from   time import time
from   view.login import login_render

"""Initialise app."""
# Set up logging.
logger = logging.getLogger(__name__)

# Set up Flask blueprint
parent_folder = os.path.dirname(os.path.abspath(__file__))
main_app = Blueprint("main_app",
                     __name__)

# initialise session
try:
    session_inst = custom_session.Session()
except IOError as e:
    logger.error(repr(e))
    # TODO: probably fix this sys.exit()...
    sys.exit()

logger.info("Loaded session.")

# Create data object to use this session
api_inst = ApiRequest()
auth_inst = Auth()

# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@main_app.route("/")
def main_page():
    """Route to login or main screen."""
    if session_inst.check_key("data_downloaded") and session_inst.select_key("data_downloaded"):
        return redirect(url_for("main_app.stats"))
    elif session_inst.check_key("logged_in") and session_inst.select_key("logged_in"):
        return redirect(url_for("main_app.get_info"))
    else:
        return redirect(url_for("main_app.login"))


@main_app.route("/login")
def login(auth_inst: Auth = auth_inst):
    """Request user info."""
    auth_url = auth_inst.generate_auth_url()
    return login_render(auth_url=auth_url)


@main_app.route("/set_info", methods=["GET"])
def set_info(api: ApiRequest = api_inst):
    """Get the token obtained from authorisation, then get the session key.

    Keyword Arguments:
        api {ApiRequest} -- (default: {api_inst})
    """
    # set the token
    new_token = request.args.get("token")
    auth_inst.get_session_key(new_token,
                              api_inst,
                              session_inst)

    return redirect(url_for("main_app.get_info"))


@main_app.route("/get_info")
def get_info(api: ApiRequest=api_inst,
             session: custom_session.Session=session_inst):
    """Load the page that displays while user info is getting fetched.

    Keyword Arguments:
        api {ApiRequest} -- (default: {api_inst})
        session {custom_session.Session} -- (default: {session_inst})
    """
    return render_template("get_info.html",
                           timestamp=time())


@main_app.route("/stats")
def stats():
    """Load main page."""
    return render_template("main_app.stats.html")
