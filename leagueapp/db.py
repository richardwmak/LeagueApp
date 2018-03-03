"""
Handles database access.
"""

import logging
import sqlite3
from   typing import Dict


# set up logging
logger = logging.getLogger(__name__)
if not __name__ == "__main__":
    # if not run from main, set up extra logging stuff
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)


class Db:
    """Handle db connections/ return query results."""

    def query(self,
              query: str="",
              params: Dict[str, str]={},
              db_name: str="league_data.db"):
        """
        Run a query (also open and close the connection).

        Args
            query - the query
            params - a dict with the parameters for the query
            db_name - database location relative to data.py

        Returns
            result: the query result as a dict of dicts
                    each subdict is a row
                    note: result == [] if sqlite finds no rows

        """
        if not db_name.endswith(".db"):
            db_name += ".db"

        logger.info("Accessing database: %s" % (db_name))

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        try:
            # open the connection
            conn = sqlite3.connect("data/" + db_name)
            conn.row_factory = dict_factory
            cursor = conn.cursor()

            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.commit()
            # close the connection
        except sqlite3.Error as e:
            logger.info("A database error has occurred: ", e.args[0])
            return False

        logger.info("Successfully ran query.")
        logger.info("Database connection closed.")
        conn.close()
        return result
