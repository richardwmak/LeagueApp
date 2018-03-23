from datetime import datetime
import logging
import sqlite3
from typing import Any, Tuple
from model.db import Db

# set up logging
logger = logging.getLogger(__name__)


class Session:
    """
    Handle sessions (because I want more control).
    """

    def __init__(self) -> None:
        """Load the Db class, initialise table.
        """
        self.db = Db()
        self.init_db()

    def init_db(self) -> Any:
        """Initialise the session db if it doesn't exist.
        """
        sql = """
            CREATE TABLE IF NOT EXISTS
                session
                (
                    key TEXT UNIQUE,
                    value TEXT,
                    date_last_access TIMESTAMP,
                    PRIMARY KEY (key)
                )
            """
        self.query(sql)

    def query(self, sql: str, params: Tuple = None, fetchall: bool = True) -> Any:
        """Run a db query with the given parameters.

        Exists to make the functions less verbose since we always need this.

        Arguments:
            sql {str} -- Query.

        Keyword Arguments:
            params -- Single parameter/ tuple of parameters (default: {None})
            fetchall {bool} -- Whether to fetchall() or fetchone() (default: {True})
        """
        try:
            result = self.db.query(sql, params, fetchall)
            return result
        except sqlite3.Error:
            raise

    def insert_key_value(self, key: str, value: Any) -> None:
        """Create a new key-value pair or update otherwise.

        Arguments:
            key {str} -- [description]

        Keyword Arguments:
            value {Any} -- [description] (default: {None})
        """
        time = datetime.now()
        # check if the key already exists
        if not self.check_key(key):
            sql = """
                INSERT INTO
                    session
                VALUES
                (?, ?, ?)
            """
            params_insert = (key, value, time)
            self.query(sql, params_insert)
        else:
            sql = """
                UPDATE
                    session
                SET
                    value = ?,
                    date_last_access = ?
                WHERE
                    key = ?
            """
            params_update = (value, time, key)
            self.query(sql, params_update)

    def delete_key(self, key: str) -> None:
        """Delete a key-value pair.

        Arguments:
            key {str} --
        """
        sql = """
            DELETE FROM
                session
            WHERE
                key = ?
        """
        params = (key,)
        self.query(sql, params)

    def select_key(self, key: str) -> Any:
        """Get the value of given a key.

        Arguments:
            key {str} --
        """
        sql = """
            SELECT
                value
            FROM
                session
            WHERE
                key = ?
        """
        params = (key,)

        value = self.query(sql, params)
        try:
            return value[0][0]
        except IndexError as e:
            logger.error(repr(e))
            raise

    def check_key(self, key: str) -> bool:
        """Check whether a key exists.

        Arguments:
            key {str} --
        """
        sql = """
            SELECT
                count(*)
            FROM
                session
            WHERE
                key = ?
        """
        params = (key,)

        result = self.query(sql, params, False)
        if result[0] == 0:
            return False
        else:
            return True

    def clear_session(self) -> None:
        """Delete all session info (i.e. drop the table).
        """
        sql = """
            DROP TABLE IF EXISTS
                session
        """

        self.query(sql)
