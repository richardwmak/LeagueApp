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
        self.token = ""

    def set_token(self, new_token: str) -> None:
        """Store the last.fm token obtained from the auth request.

        Arguments:
            token {str} --
        """
        self.token = new_token

    def init_user(self, username: str, region: str):
        """Set user variables.

        Arguments:
            username {str} --
            region {str} --
        """
        self.username = username

    def get_data_from_url(self, url: str) -> Tuple[str, int]:
        """
        Get data from last.fm API.

        It is always of the form

        http://ws.audioscrobbler.com/2.0/

        Arguments:
            self.region --
            self.api_key --
            url -- location of the data (i.e. API_CATEGORY)

        Returns:
            Tuple[str, int] -- the decoded json data, HTML status code resp.
        """
        logger.info("Attempting to connect to last.fm API.")
        complete_url = "http://ws.audioscrobbler.com/2.0/"  # TODO
        headers = {"X-Riot-Token": self.api_key}
        logger.info("URL: %s" % complete_url)
        try:
            http_response = requests.get(
                complete_url,
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
