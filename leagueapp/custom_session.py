import logging
from   pathlib import Path
import pickle
from   typing import Any


# set up logging
logger = logging.getLogger(__name__)


class Session:
    """
    Handle sessions (because I want more control).
    """

    def __init__(self, session_file_path: str="data/session.p") -> None:
        """Load the initial session.

        Keyword Arguments:
            session_file_path {str} -- (default: {"data/session.p"})
        """
        self.session = {}  # type: dict
        self.session_file_path = session_file_path
        if Path(self.session_file_path).is_file():
            self.load_session()

    def save_session(self):
        """
        Save the session dict using pickle.
        """
        with open(self.session_file_path, mode="w") as f:
            try:
                pickle.dump(self.session, f)
            except pickle.PickleError as e:
                logger.error("Failed to save session.")
                raise SessionSaveException("Failed to save session.")

    def load_session(self):
        """
        Load the session dict using pickle.
        """
        with open(self.session_file_path, mode="r") as f:
            try:
                self.session = pickle.load(f)
            except pickle.PickleError as e:
                logger.error("Failed to load session.")
                raise SessionLoadException("Failed to load session.")

    def insert_key_value(self, key: str, value: Any = None):
        """Add key-value pair to the session.

        Arguments:
            key {str} --

        Keyword Arguments:
            value {Any} -- (default: {None})
        """
        # TODO: change behaviour depending on whether key exists?
        self.session[key] = value

    def delete_key(self, key: str):
        """Delete a key-value pair.

        Arguments:
            key {str} --
        """
        # None is specified because otherwise a KeyError is raised if given key
        # does not exist.
        self.session.pop(key, None)

    def select_key(self, key: str) -> Any:
        """Return value given a key.

        Arguments:
            key {str} --

        Returns:
            value {Any} -- the value for the key
        """
        try:
            value = self.session[key]
        except KeyError as e:
            logger.error("Key doesn't exist.")
            raise SessionKeyException("Key doesn't exist.")
        return value

    def check_key(self, key: str) -> bool:
        """Check if key exists.

        Arguments:
            key {str} --

        Returns:
            bool -- True/false depending on existence.
        """
        if key in self.session:
            return True
        else:
            return False

    def clear_session(self):
        """Delete the entire dict.
        """
        self.session.clear()


class SessionLoadException(Exception):  # noqa
    pass


class SessionSaveException(Exception):  # noqa
    pass


class SessionKeyException(Exception):  # noqa
    pass
