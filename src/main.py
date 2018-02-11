""" Main file 

.\virtual\Scripts\python.exe .\src\main.py
"""

import datetime
from   flask import Flask, request, redirect, url_for, render_template
import logging
import sys

app = Flask(__name__)


def setup_app():
    # set up logging
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
    logging.info("\nSTART UP")
    logging.info("Date/time: %s\n" % (datetime.datetime.now()))

setup_app()

@app.route("/")
def main_page():
    if not "username" in request.cookies:
        return redirect(url_for("login"))
    else:
        pass

@app.route("/login")
def login():
    # hardcoded a list of regions, don't know a better way right now
    region_list = ["RU", "KR", "BR1", "OC1", "JP1", "NA1", "EUN1", "EUW1", "TR1", "LA1", "LA2"]
    return render_template("login.html", region_list=region_list)



if __name__ == "__main__":
    app.run()