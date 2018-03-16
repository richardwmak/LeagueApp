from   _version import __version__
import configparser
import logging
import requests
from   typing import Tuple

# set up logging
logger = logging.getLogger(__name__)


class ApiRequest:
    """
    Handles the API requests and data storage.
    """

###############################################################################
# INITIALIZATION METHODS
###############################################################################

    def __init__(self):
        """Get api key from ini.

        TODO: somehow do this in a sensible way when in prod
        """
        config = configparser.ConfigParser()
        config.read("secrets.ini")

        self.version = __version__
        self.api_key = config["api"]["key"]
        self.session_key = ""
        self.last_request = None

    def set_session_key(self, session_key: str) -> None:
        """Store the last.fm token obtained from the auth request.

        Arguments:
            token {str} --
        """
        self.session_key = session_key

    def get_data_from_url(self, param_dict: dict = {}, use_json: bool = True) -> Tuple[dict, int]:
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

            if status_code is 200:
                logger.info("Successfully retrieved data.")
            else:
                logger.error("Failed to retrieve data. HTTP error code: %s" % status_code)

            return data, status_code

        except requests.HTTPError as e:
            logger.info("An HTTP error has occured: %s" % e)
            return None, 0

        except requests.Timeout as e:
            logger.info("Connection timed out: %s" % e)
            return None, 0

        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s" % e)
            return None, 0
