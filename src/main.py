""" Main file """

import datetime
import logging
from PyQt5.QtWidgets import QApplication
import sys
from view import MainWindow

def main():
    # set up logging
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
    logging.info("\nSTART UP")
    logging.info("Date/time: %s\n" % (datetime.datetime.now()))

    # UI stuff
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()