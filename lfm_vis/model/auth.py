import configparser
import hashlib
import logging

from model.custom_session import Session
from model.api import ApiRequest

# set up logging
logger = logging.getLogger(__name__)


class Auth():
    """Get last.fm authorisation.
    """

    def __init__(self) -> None:  # noqa

        self.username = ""
        self.auth_url = ""

        config = configparser.ConfigParser()
        config.read("secrets.ini")
        self.api_key = config["api"]["key"]  # type: str
        self.secret = config["api"]["secret"]  # type: str

    def generate_auth_url(
            self, callback_url: str = "http://localhost:5000/set_info") -> str:
        """Generate the url to get last.fm authorisation for user.

        Keyword Arguments:
            callback_url {str} -- url to send the user to after finishing
                authorization (default: {"http://localhost:5000/set_info"})

        Returns:
            str --
        """
        self.auth_url = "http://www.last.fm/api/auth/?api_key=%s&cb=%s" % (
            self.api_key, callback_url)

        return self.auth_url

    def generate_getsession_param_dict(self, token: str) -> dict:
        """Generate the dictionary of parameters to call auth.getSession.

        Arguments:
            token {str} -- Token return by initial authorisation.
        """
        md5_hash = hashlib.md5()
        string_to_hash = "api_key%smethodauth.getSessiontoken%s%s" % (
            self.api_key, token, self.secret)
        md5_hash.update(string_to_hash.encode('utf-8'))
        api_sig = md5_hash.hexdigest()

        param_dict = {
            "token": token,
            "api_sig": api_sig,
            "method": "auth.getSession"
        }

        return param_dict

    def get_session_key(self, token: str, api_request_instance: ApiRequest,
                        session: Session) -> None:
        """Get the session key and username given a token.

        Arguments:
            token {str} --
            api_request_instance {ApiRequest} --
            session {Session} --
        """
        # get the session key
        param_dict = self.generate_getsession_param_dict(token)
        (data,
         _status_code) = api_request_instance.get_data_from_url(param_dict)

        if "error" in data:
            logger.error("API request returned error: %s", data["message"])
            raise Exception("API request returned error: %s" % data["message"])

        logger.info(data)

        session_key = data["session"]["key"]
        api_request_instance.set_session_key(session_key)
        session.insert_key_value("session_key", session_key)

        username = data["session"]["name"]
        session.insert_key_value("username", username)

        session.insert_key_value("logged_in", True)
