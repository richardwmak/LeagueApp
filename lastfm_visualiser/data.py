from  ._version import __version__
import configparser
import logging
import os
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
        secrets_path = os.path.dirname(__file__) + "\secrets.ini"

        config.read(secrets_path)

        self.version = __version__
        self.api_key = config["api"]["key"]
        self.session_key = ""
        self.username = ""
        self.last_request = None

    def set_session_key(self, session_key: str) -> None:
        """Store the last.fm token obtained from the auth request.

        Arguments:
            token {str} --
        """
        self.session_key = session_key

    def set_username(self, username: str) -> None:
        """Set the username

        Arguments:
            username {str} --
        """
        self.username = username

    def init_user(self, username: str, region: str):
        """Set user variables.

        Arguments:
            username {str} --
            region {str} --
        """
        self.username = username

    def generate_api_url(self, method_params: dict = {}, use_json: bool = True) -> str:
        """Generate the URL to be used for the api request.

        Keyword Arguments:
            method_params {dict} -- parameters for the GET request (default: {{}})
            use_json {bool} -- whether or not to use JSON instead of the default XML (default: {True})

        Returns:
            str -- the generated URL
        """
        param_dict = {}
        if use_json is True:
            param_dict["format"] = "json"

        for key, value in method_params.items():
            param_dict[key] = value

        params = "?api_key=%s" % self.api_key
        for key, value in param_dict.items():
            params += "&%s=%s" % (key, value)

        complete_url = "http://ws.audioscrobbler.com/2.0/%s" % params

        return complete_url

    def get_data_from_url(self, method_params: dict = {}, use_json: bool = True) -> Tuple[dict, int]:
        """Perform the actual api request.

        Keyword Arguments:
            method_params {dict} -- parameters for the GET request (default: {{}})
            use_json {bool} -- whether or not to use JSON (default: {True})

        Returns:
            Tuple[str, int] -- data/ response code
        """
        logger.info("Attempting to connect to last.fm API.")

        complete_url = self.generate_api_url(method_params, use_json)
        headers = {"User-Agent": "lastfm_visualiser v%s" % self.version}

        logger.info("URL: %s" % complete_url)
        try:
            http_response = requests.get(url=complete_url,
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
