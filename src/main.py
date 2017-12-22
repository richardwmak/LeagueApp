""" Main file """

import logging
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from view import MainWindow, Sidebar

def main():
    # set up logging
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    sidebar = Sidebar(window)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()