r"""
Main file.

.\virtual\Scripts\python.exe .\src\main.py
"""

from   .data import ApiRequest
import datetime
from   flask import Flask, request, redirect, url_for, render_template
import json
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
try:
    session.load_session()
except custom_session.SessionLoadException():
    logging.error("Failed to load session.")

# Set up logging.
# Clear old log:
with open("LeagueApp.log", "w"):
    pass

logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
logging.info("\nSTART UP")
logging.info("Date/time: %s\n" % (datetime.datetime.now()))

# Create data object to use this session
api_request_instance = ApiRequest()

# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@app.route("/")
def main_page():
    """Route to login or main screen."""
    if "logged_in" in session and session["logged_in"] is True:
        return redirect(url_for("stats"))
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login():
    """Request user info."""
    region_list = {"RU": "Russia", "KR": "Korea", "BR1": "Brazil",
                   "OC1": "Oceania", "JP1": "Japan", "NA1": "NA",
                   "EUN1": "EUN", "EUW1": "EUW", "TR1": "Turkey",
                   "LA1": "LA1", "LA2": "LA2"}

    # sort region_list
    keys = sorted(region_list)
    region_list_sorted = {}
    for key in keys:
        region_list_sorted[key] = region_list[key]

    return render_template("login.html",
                           region_list=region_list_sorted,
                           timestamp=int(time.time()))


@app.route("/set_info", methods=["POST"])
def set_info(api: ApiRequest = api_request_instance):
    """Check if user exists via ajax request.

    Keyword Arguments:
        api {ApiRequest} -- API request object of choice (default: {api_request_instance})
    """
    username = request.json["username"]
    region = request.json["region"]

    # TODO: break out authorization
    api.init_user(username, region)
    (data, status_code) = api.get_account_data()

    if status_code is not 200:
        message = "This combination of username and password was not found."
        result = json.dumps({"success": False,
                             "message": message})
        session["logged_in"] = False
        logging.info("Failed to log in.")
    else:
        session["username"] = request.json["username"]
        session["region"] = request.json["region"]
        session["logged_in"] = True

        result = json.dumps({"success": True,
                             "message": None})
        logging.info("Successfully logged in.")

    return result


@app.route("/stats")
def stats():
    """Load main page."""
    data = ApiRequest()

    data.init_user(session["username"], session["region"])

    # return render_template("stats.html",
    #                        )


if __name__ == "__main__":
    app.run()
