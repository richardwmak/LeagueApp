r"""
Main file.

.\virtual\Scripts\python.exe .\src\main.py
"""
from   .auth import GetAuth
from   .data import ApiRequest
import datetime
from   flask import Flask, redirect, request, url_for, render_template
import logging
import custom_session
import time


"""Initialise app."""

# Set up Flask app.
app = Flask(__name__)
app.secret_key = ('\xd5\x99\x98N\x1e\xac7\xc9{\x9d\xdc\xefN\xdf\xcbR\xfc\x8f' +
                  '\xfa$\xa1\xa7\xd7j')

# initialise session
session = custom_session.Session()

# Set up logging.
# Clear old log:
with open("LeagueApp.log", "w"):
    pass

logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
logging.info("\nSTART UP")
logging.info("Date/time: %s\n" % (datetime.datetime.now()))

# Create data object to use this session
api_request_instance = ApiRequest()
auth_instance = GetAuth()

# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@app.route("/")
def main_page():
    """Route to login or main screen."""
    if session.check_key("logged_in") and session.select_key("logged_in") is True:
        return redirect(url_for("stats"))
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login(auth_instance: GetAuth = auth_instance):
    """Request user info."""
    auth_url = auth_instance.generate_auth_url()

    return render_template("login.html",
                           auth_url=auth_url,
                           timestamp=int(time.time()))


@app.route("/auth")
def auth_page():
    """Handle last.fm authorisation.
    """
    pass


@app.route("/set_info", methods=["GET"])
def set_info(api: ApiRequest = api_request_instance):
    """Set the token obtained from authorisation.

    Keyword Arguments:
        api {ApiRequest} -- (default: {api_request_instance})
    """
    new_token = request.args.get("token")

    api_request_instance.set_token(new_token)
    session.insert_key_value("logged_in", True)
    
    redirect(url_for("stats"))


@app.route("/stats")
def stats():
    """Load main page."""
    data = ApiRequest()

    curr_user = session.select_key("username")
    curr_region = session.select_key("region")

    data.init_user(curr_user, curr_region)

    return render_template("stats.html")


if __name__ == "__main__":
    app.run()
