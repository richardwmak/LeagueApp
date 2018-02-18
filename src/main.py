""" Main file 

.\virtual\Scripts\python.exe .\src\main.py
"""

from   data import ApiRequest
import datetime
import time
from   flask import Flask, request, redirect, url_for, render_template, session
import logging
import sys

app = Flask(__name__)
app.secret_key = '\xd5\x99\x98N\x1e\xac7\xc9{\x9d\xdc\xefN\xdf\xcbR\xfc\x8f\xfa$\xa1\xa7\xd7j'

def setup_app():
    # set up logging
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
    logging.info("\nSTART UP")
    logging.info("Date/time: %s\n" % (datetime.datetime.now()))

setup_app()


# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@app.route("/")
def main_page():
    if not "username" in session or not "region" in session:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("stats"))


@app.route("/login")
def login():
    # hardcoded a list of regions, don't know a better way right now
    # TODO: improve server names
    region_list = sorted(["RU", "KR", "BR1", "OC1", "JP1", "NA1", "EUN1", "EUW1", "TR1", "LA1", "LA2"])
    return render_template("login.html", region_list=region_list, timestamp=int(time.time()))


@app.route("/set_info", methods=["POST"])
def set_info():
    session["username"] = request.form("username")
    session["region"] = request.form("region")

    return redirect(url_for("stats"))


@app.route("/stats")
def stats():
    if not "username" in session or not "region" in session:
        return redirect(url_for("login"))
    else:
        pass


if __name__ == "__main__":
    app.run()