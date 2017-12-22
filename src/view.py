"""
Main GUI code
"""
import logging
from PyQt5.QtWidgets import QWidget, QPushButton

# set up logging
logger = logging.getLogger(__name__)
if not __name__ == "__main__":
    # if not run from main, set up extra logging stuff
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)

class CustomWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.set_parent(parent)

        logger.info("Initializing window: %s" % self.__class__.__name__)


    def open_stylesheet(self, filename):
        logger.info('Accessing stylesheet: %s' % (filename))

        try:
            with open(filename) as stylesheet:
                self.setStyleSheet(stylesheet.read())
                
                logger.info('Loaded stylesheet')
        except EnvironmentError as e:
            logger.info('Error accessing stylesheet: %s' % (e.args[0]))

    def set_parent(self, parent):
        if not parent == None:
            self.setParent(parent)


class MainWindow(CustomWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 800)
        self.move(300,300)
        self.setWindowTitle('LeagueApp')

        self.open_stylesheet('style/main.qss')

        self.show()
        

class Sidebar(CustomWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0,0,100,500)

        self.open_stylesheet('style/sidebar.qss')
        self.add_button()

        self.show()

    def add_button(self):
        btn = QPushButton('Yo', self)
        btn.resize(btn.sizeHint())
        btn.move(10,10)


class Header:
    pass

class Content:
    pass
