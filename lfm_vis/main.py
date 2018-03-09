from   controller.controller import start_server
import datetime
import logging
import requests
from   threading import Thread
from   time import sleep
import webview


def run_app():  # noqa
    t = Thread(target=start_server)
    t.daemon = True
    t.start()

    # https://stackoverflow.com/a/15743618
    # https://github.com/r0x0r/pywebview/blob/master/examples/flask_app/src/backend/main.p
    url_accessible = False
    while not url_accessible:
        try:
            r = requests.head("http://127.0.0.1:5000")
            status_code = r.status_code
            if status_code == 200:
                url_accessible = True
        except requests.RequestException:
            url_accessible = False

        sleep(0.5)

    webview.create_window("test", "http://127.0.0.1:5000")


if __name__ == "__main__":
    # set up logging
    # https://docs.python.org/3/howto/logging-cookbook.html
    logger = logging.getLogger(__name__)
    logger_werkzeug = logging.getLogger("werkzeug")
    logger.setLevel(logging.DEBUG)
    logger_werkzeug.setLevel(logging.DEBUG)

    fh = logging.FileHandler("app.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger_werkzeug.addHandler(fh)
    logger.addHandler(ch)
    logger_werkzeug.addHandler(ch)

    logger.info("START UP")
    logger.info("Date/time: %s\n" % (datetime.datetime.now()))

    start_server()

    # TODO: only use if not developing

    # run_app()
