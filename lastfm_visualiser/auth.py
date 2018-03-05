import configparser
import logging


# set up logging
logger = logging.getLogger(__name__)


class GetAuth():
    """Get last.fm authorisation.
    """

    def __init__(self):  # noqa

        self.username = ""
        self.auth_url = ""

        config = configparser.ConfigParser()
        config.read("secrets.ini")
        self.api_key = config["api"]["key"]

    def generate_auth_url(self, callback_url: str = "http://localhost:5000/set_info") -> str:
        """Generate the url to get last.fm authorisation for user.

        Keyword Arguments:
            callback_url {str} -- url to send the user to after finishing authorization (default: {"http://localhost:5000/set_info"})

        Returns:
            str -- [description]
        """
        self.auth_url = "http://www.last.fm/api/auth/?api_key=%s&cb=%s" % (self.api_key, callback_url)

        return self.auth_url
