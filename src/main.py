""" Main file """

import datetime
from   flask import Flask
import logging
import sys

app = Flask(__name__)


def setup_app():
    # set up logging
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
    logging.info("\nSTART UP")
    logging.info("Date/time: %s\n" % (datetime.datetime.now()))

setup_app()

@app.route('/')
def main_page():
    



if __name__ == "__main__":
    app.run()