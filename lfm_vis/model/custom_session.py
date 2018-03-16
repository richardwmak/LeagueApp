import logging
import pickle
from   typing import Any


# set up logging
logger = logging.getLogger(__name__)


class Session:
    """
    Handle sessions (because I want more control).
    """

    def __init__(self, session_file_path: str="model/data/session.p") -> None:
        """Load the initial session.

        Keyword Arguments:
            session_file_path {str} -- (default: {"data/session.p"})
        """
        self.session = {}  # type: dict
        self.session_file_path = session_file_path
        # check if file exists
        try:
            self.load_session()
        except (OSError, EOFError):
            pass

    def save_session(self):
        """
        Save the session dict using pickle.
        """
        with open(self.session_file_path, mode="wb") as f:
            try:
                pickle.dump(self.session, f)
            except pickle.PickleError as e:
                logger.error("Failed to save session.")
                raise SessionSaveException("Failed to save session.")

    def load_session(self):
        """
        Load the session dict using pickle.
        """
        try:
            with open(self.session_file_path, mode="rb") as f:
                try:
                    self.session = pickle.load(f)
                except pickle.PickleError as e:
                    logger.error("Failed to load session.")
                    raise SessionLoadException("Failed to load session.")
                except TypeError:
                    # a TypeError will occur if the file is empty as pickle expects
                    # a bytes-like object. In such a case, we just want an empty dict
                    self.session = {}
                except EOFError:
                    logger.error(repr(EOFError))
                    raise
        except OSError:
            logger.info("Failed to open session.p")
            raise

    def insert_key_value(self, key: str, value: Any = None):
        """Add key-value pair to the session.

        Arguments:
            key {str} --

        Keyword Arguments:
            value {Any} -- (default: {None})
        """
        # TODO: change behaviour depending on whether key exists?
        self.session[key] = value
        self.save_session()

    def delete_key(self, key: str):
        """Delete a key-value pair.

        Arguments:
            key {str} --
        """
        # None is specified because otherwise a KeyError is raised if given key
        # does not exist.
        self.session.pop(key, None)
        self.save_session()

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
        self.save_session()


class SessionLoadException(BaseException):  # noqa
    pass


class SessionSaveException(BaseException):  # noqa
    pass


class SessionKeyException(BaseException):  # noqa
    pass
