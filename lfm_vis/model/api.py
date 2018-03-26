import configparser
import logging
from typing import Dict, Tuple

import requests

from _version import __version__
from tools.decorators import retry
from model.custom_session import Session

# set up logging
logger = logging.getLogger(__name__)


class ApiRequest:
    """
    Handles the API requests and data storage.
    """

    def __init__(self) -> None:
        """Get api key from ini.

        TODO: somehow do this in a sensible way when in prod
        """
        config = configparser.ConfigParser()
        config.read("secrets.ini")

        self.version = __version__
        self.api_key = config["api"]["key"]
        self.session_key: str
        session = Session()

        if session.check_key("session_key"):
            self.session_key = session.select_key("session_key")

    def set_session_key(self, session_key: str) -> None:
        """Store the last.fm token obtained from the auth request.

        Arguments:
            token {str} --
        """
        self.session_key = session_key

    @retry(3, 1, requests.Timeout)
    def get_data_from_url(self, param_dict: Dict, use_json: bool = True) -> Tuple[Dict, int]:
        """Perform the actual api request.

        Keyword Arguments:
            param_dict {dict} -- parameters for the GET request (default: {{}})
            use_json {bool} -- whether or not to use JSON (default: {True})

        Returns:
            Tuple[str, int] -- data/ response code
        """
        base_url = "http://ws.audioscrobbler.com/2.0/"
        param_dict["api_key"] = self.api_key
        if use_json is True:
            param_dict["format"] = "json"

        logger.info("Attempting to connect to last.fm API.")
        headers = {"User-Agent": "lastfm_visualiser v%s" % self.version}

        try:
            http_response = requests.get(url=base_url,
                                         params=param_dict,
                                         headers=headers)
            data = http_response.json()
            status_code = http_response.status_code

            if status_code == 200:
                logger.info("Successfully retrieved data.")
            else:
                logger.error("Failed to retrieve data. HTTP error code: %s", status_code)

            return data, status_code

        except requests.HTTPError as e:
            logger.info("An HTTP error has occured: %s", e)
            return ({"error": True}, 0)
        except requests.Timeout as e:
            logger.info("Connection timed out: %s", e)
            raise
        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s", e)
            return ({"error": True}, 0)
