import logging
import threading
import time
from typing import Any

from flask import Blueprint, jsonify

from model.custom_session import Session
from model.listen_history import ListenHistory

# Set up logging.
logger = logging.getLogger(__name__)

# set up blueprint
AJAX_APP = Blueprint("AJAX_APP", __name__)

# set up classes
SESSION = Session()

# TODO: actually do this right (MVC)


def listen_history_download_process() -> None:
    """Control the history download.
    """
    listen_history = ListenHistory()
    logger.info("Started listen history download.")
    SESSION.insert_key_value("listen_history.continue_dl", True)

    while (listen_history.current_page <= listen_history.total_pages and
           int(SESSION.select_key("listen_history.continue_dl"))) == 1:
        try:
            listen_history.generate_data()
            listen_history.generate_query_params()
            listen_history.store_data()
            listen_history.store_current_page()
        except Exception:
            time.sleep(1)
            continue

        time.sleep(1)


@AJAX_APP.route("/ajax/listen_history_download", methods=["POST"])
def listen_history_download() -> Any:
    """Set the downloader to run in a thread and return this to the js.
    """
    thread = threading.Thread(target=listen_history_download_process, args=())
    thread.start()
    result = {"success": True, "message": None}

    return jsonify(result)


@AJAX_APP.route("/ajax/listen_history_progress", methods=["POST"])
def listen_history_progress() -> Any:
    """Check the current download progress.
    """
    current_page = int(SESSION.select_key("listen_history.current_page"))
    total_pages = int(SESSION.select_key("listen_history.total_pages"))

    result = {"current_page": current_page, "total_pages": total_pages}

    return jsonify(result)


@AJAX_APP.route("/ajax/listen_history_pause", methods=["POST"])
def listen_history_pause() -> Any:
    """Stop the history download.
    """
    SESSION.insert_key_value("listen_history.continue_dl", False)
    result = {"success": True, "message": None}
    logger.info("Stop listen history download.")

    return jsonify(result)
