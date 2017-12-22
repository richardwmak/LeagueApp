"""
Main GUI code
"""
import logging
from PyQt5.QtWidgets import QFrame, QGridLayout, QMainWindow, QWidget

# set up logging
logger = logging.getLogger(__name__)
if not __name__ == "__main__":
    # if not run from main, set up extra logging stuff
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)


class UiFunctions():
    def __init__(self):
        logger.info("Initializing window: %s" % self.__class__.__name__)


    def open_stylesheet(self, filename):
        logger.info('Accessing stylesheet: %s' % (filename))

        try:
            with open(filename) as stylesheet:
                self.setStyleSheet(stylesheet.read())
                
                logger.info('Loaded stylesheet')
        except EnvironmentError as e:
            logger.info('Error accessing stylesheet: %s' % (e.args[0]))


class Sidebar(QWidget, UiFunctions):
    def __init__(self):
        super().__init__()

        self.init_ui()

    
    def init_ui(self):
        square = QFrame(self)
        square.setGeometry(0,0,200,200)
        square.setStyleSheet("background: red")

        self.show()


class Header(QWidget, UiFunctions):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        square = QFrame(self)
        square.setGeometry(0,0,200,200)
        square.setStyleSheet("background: blue")

        self.show()


class Content(QWidget, UiFunctions):
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        square = QFrame(self)
        square.setGeometry(0,0,200,200)
        square.setStyleSheet("background: green")

        self.show()
        

class CentralWidget(QWidget, UiFunctions):
    """
    Contains (currently) all of the UI. Just there for the
    gridlayout
    """
    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        # horizontal grid contains sidebar and content
        grid = QGridLayout(self)
        grid.setSpacing(1)

        sidebar = Sidebar()
        content = Content()
        header = Header()

        grid.addWidget(header,  0, 0, 1, -1)
        grid.addWidget(sidebar, 1, 0, 1,  1)
        grid.addWidget(content, 1, 1, 1,  1)

        self.show()


class MainWindow(QMainWindow, UiFunctions):
    """
    The container of the GUI.
    Currently making it a QMainWindow doesn't do much. It is
    mainly there to allow for a certain UI structure afaik:
    https://doc.qt.io/qt-5/qmainwindow.html
    
    I don't see a reason not to use it.
    """
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.open_stylesheet('data/main.qss')

        central_widget = CentralWidget()
        self.setCentralWidget(central_widget)
        self.setGeometry(300,300,800,800)
        self.setWindowTitle('LeagueApp')

        self.show()