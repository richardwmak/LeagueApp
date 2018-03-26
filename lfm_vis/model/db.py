"""
Handles database access.
"""
import logging
import sqlite3
from typing import Any, Tuple

from tools.decorators import retry

# set up logging
logger = logging.getLogger(__name__)


class Db:
    """Handle db connections/ return query results."""

    def __init__(self, db_name: str = "lfm_vis_data.db") -> None:
        """Initialise class.

        Keyword Arguments:
            db_name {str} -- DB to access (default: {"lfm_vis_data.db"})
        """
        self.db_name = db_name
        self.open_connection = False
        self.conn = None  # type: Any
        self.cursor = None  # type: Any
        # very naive input checking
        if not self.db_name.endswith(".db"):
            self.db_name += ".db"

    def connect(self) -> None:
        """Open database connection.
        """
        if self.open_connection is True:
            raise Exception("Database already has open connection.")

        logger.info("Opening database connection.")
        try:
            self.conn = sqlite3.connect(
                "model/data/" + self.db_name, check_same_thread=False)
        except sqlite3.Error as e:
            logger.error("Failed to open database connection: %s", repr(e))
            raise

        self.open_connection = True

    def disconnect(self) -> None:
        """Close database connection.
        """
        if self.open_connection is False:
            raise Exception(
                "Database object does not have a connection to close.")

        logger.info("Closing database connection.")
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logger.error("Failed to close database connection: %s", repr(e))
            raise

        self.open_connection = False

    def execute_query(self, sql: str, params: Tuple = None) -> None:
        """Execute the query.
        """
        if self.open_connection is False:
            raise Exception("Tried to run query while connection was closed.")

        self.cursor = self.conn.cursor()
        try:
            if params is None:
                self.cursor.execute(sql)
            elif isinstance(params, list):
                self.cursor.executemany(sql, params)
            else:
                self.cursor.execute(sql, params)
        except sqlite3.Error as e:
            logger.error("Failed to execute query: %s", repr(e))
            raise

        try:
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error("Failed to commit query: %s", repr(e))
            raise

    def fetch_results_all(self) -> Any:
        """Return query results using fetchall().
        """
        try:
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error("Failed to fetch results: %s", repr(e))
            raise

    def fetch_results_one(self) -> Any:
        """Return query results using fetchone().
        """
        try:
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error("Failed to fetch results: %s", repr(e))
            raise

    @retry(5, 1, Exception)
    def query(self, sql: str = "", params: Tuple = None,
              fetchall: bool = True) -> Any:
        """Shorthand for running a full query.
        """
        self.connect()
        self.execute_query(sql, params)
        if fetchall:
            results = self.fetch_results_all()
        else:
            results = self.fetch_results_one()
        self.disconnect()

        return results
