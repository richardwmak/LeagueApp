from   controller.controller import main_app
from   flask import Flask
import logging


if __name__ == "__main__":
    # set up logging
    # https://docs.python.org/3/howto/logging-cookbook.html
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("app.log", mode="w+")
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s\n%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    app = Flask(__name__,
                static_folder="view/static",
                template_folder="view/templates")
    app.register_blueprint(main_app)

    app.run(debug=True, port=5000)
