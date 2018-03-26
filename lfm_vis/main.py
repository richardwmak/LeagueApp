import logging

from controller.controller import MAIN_APP
from controller.ajax import AJAX_APP
from flask import Flask


if __name__ == "__main__":
    # set up logging
    # https://docs.python.org/3/howto/logging-cookbook.html
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    FH = logging.FileHandler("app.log", mode="w+")
    CH = logging.StreamHandler()

    FORMATTER = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s\n%(message)s')
    FH.setFormatter(FORMATTER)
    CH.setFormatter(FORMATTER)

    logger.addHandler(FH)
    logger.addHandler(CH)
    logger.setLevel(logging.DEBUG)

    APP = Flask(__name__,
                static_folder="view/static",
                template_folder="view/templates")
    APP.register_blueprint(MAIN_APP)
    APP.register_blueprint(AJAX_APP)

    APP.run(debug=True, port=5000, threaded=True)
