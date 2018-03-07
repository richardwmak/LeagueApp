import configparser
import hashlib
import logging


# set up logging
logger = logging.getLogger(__name__)


class Auth():
    """Get last.fm authorisation.
    """

    def __init__(self):  # noqa

        self.username = ""
        self.auth_url = ""

        config = configparser.ConfigParser()
        config.read("secrets.ini")
        self.api_key = config["api"]["key"]  # type: str
        self.secret = config["api"]["secret"]  # type: str

    def generate_auth_url(self, callback_url: str = "http://localhost:5000/set_info") -> str:
        """Generate the url to get last.fm authorisation for user.

        Keyword Arguments:
            callback_url {str} -- url to send the user to after finishing authorization (default: {"http://localhost:5000/set_info"})

        Returns:
            str -- [description]
        """
        self.auth_url = "http://www.last.fm/api/auth/?api_key=%s&cb=%s" % (self.api_key, callback_url)

        return self.auth_url

    def generate_getsession_param_dict(self, token: str) -> dict:
        """Generate the dictionary of parameters to call auth.getSession.

        Arguments:
            token {str} -- Token return by initial authorisation.
        """
        hash = hashlib.md5()
        string_to_hash = "api_key%smethodauth.getSessiontoken%s%s" % (self.api_key, token, self.secret)
        hash.update(string_to_hash.encode('utf-8'))
        api_sig = hash.hexdigest()

        param_dict = {"token": token,
                      "api_sig": api_sig,
                      "method": "auth.getSession"}

        return param_dict
