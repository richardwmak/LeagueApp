"""Handles the API requests and data storage.

Test commands:

from importlib import reload
import sys

if "data" in sys.modules:
    reload(data)
else:
    import data

data1 = data.ApiRequest("reeepicheeep", "EUW1")
"""

import logging
import requests
import sqlite3
from   typing import Any, Dict

# set up logging
logger = logging.getLogger(__name__)
if not __name__ == "__main__":
    # if not run from main, set up extra logging stuff
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)


class ApiRequest:
    """TODO: write docstring."""

###############################################################################
# INITIALIZATION METHODS
###############################################################################

    def __init__(self):
        """
        Initialize various relevant variables (surprise, surprise).

        Args:
            username: League of Legends username
            region: Account region
        """
        self.api_key = "RGAPI-e7f9f9d4-20d7-4811-865f-4ce59d0efd04"
        self.version = None
        self.account_data = []

        # self.initialize_db()
        # set_version() both checks the version and run and get_champion_list()
        # if the version is different
        # self.set_version()

    def init_user(self, username: str, region: str):
        """Store user info."""
        self.username = username
        self.region = region

    def initialise_db(self):
        """Create empty database with relevant tables if they don't exist."""
        table_dict = {}
        table_dict['info'] = ['version TEXT PRIMARY KEY ASC']
        table_dict['champion'] = ['key INTEGER PRIMARY KEY', 'name TEXT']

###############################################################################
        """
        Table name: info
        Columns:
            version - league version
                text
                primary key
        """
        sql = """
            CREATE TABLE IF NOT EXISTS
                "info"
                (
                    "version" TEXT PRIMARY KEY ASC
                )
            """
        Db.query(sql)
###############################################################################
        """
        Table name: champion
        Columns:
            key - champion key (unique)
                text
                primary key
            name - champion name
                text
            id - champion numerical id
                integer
            title - champion title
                text
        """
        sql = """
            CREATE TABLE IF NOT EXISTS
                "champion"
                (
                    "key" TEXT PRIMARY KEY ASC,
                    "name" TEXT,
                    "id" INTEGER,
                    "title" TEXT
                )
            """
        Db.query(sql)
###############################################################################

    def update_league_version(self):
        """Check if the current league version matches the stored one."""
        # get stored value
        sql = """
            SELECT
                "version"
            FROM
                "info"
            """

        # for some result query returns e.g. [('7.24.2',)]
        local_version = Db.query(sql)[0][0]

        # get current value
        # https://ddragon.leagueoflegends.com/api/versions.json is a list of
        # all version with the first entry being the current version
        try:
            http_response = requests.get(
                "https://ddragon.leagueoflegends.com/api/versions.json")
            data = http_response.json()

        except requests.HTTPError as e:
            logger.info("An HTTP error has occured: %s" % e.reason)
            return False

        except requests.Timeout as e:

            logger.info("Connection timed out: %s" % e.reason)
            return False

        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s" % e.reason)
            return False
        riot_version = data[0]

        if riot_version == local_version:
            # if the versions are the same, we can assume everything has
            # updated just fine
            print("LeagueApp is up to date.")
            return
        else:
            # if not, we need to update some stuff

            # different queries depending on if the row exists
            if local_version == []:
                sql = """
                    INSERT INTO
                        'info' (version)
                    VALUES
                        (:version)
                    """
            else:
                sql = """
                    UPDATE
                        'info'
                    SET
                        'version' = :version
                    """

            params = {"version": riot_version}

            result = Db.query(sql, params)

            if result is False:
                print("Version could not be updated.")
            else:
                print("Version successfully updated.")

            self.update_champion()

    def get_data_from_url(self, url: str):
        """
        Get data from Riot API.

        It is always of the form

        https://REGION.api.riotgames.com/lol/API_CATEGORY?api_key=API_KEY

        Args:
            self.region
            self.api_key
            url: location of the data (i.e. API_CATEGORY)

        Returns:
            data: the decoded json data

        """
        logger.info("Attempting to connect to Riot API.")
        try:
            http_response = requests.get(
                "https://" + self.region + ".api.riotgames.com/lol/" + url,
                headers={"X-Riot-Token": + self.api_key})
            data = http_response.json()

            logger.info("Successfully retrieved data.")
            return data

        except requests.HTTPError as e:
            logger.info("An HTTP error has occured: %s" % e)
            return False

        except requests.Timeout as e:

            logger.info("Connection timed out: %s" % e)
            return False

        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s" % e)
            return False

    def update_champion(self):
        """
        Get champion names and IDs and puts them into the champion table.

        Args:

        Returns:

        """
        # the format of data is
        # data
        # |-- type: "champion"
        # |-- version: current version
        # |-- data
        #     |-- champion_first_data
        #     |-- ...
        #     |-- champion_last_data
        data = self.get_data_from_url("static-data/v3/champions")["data"]

        # sort all the info by key
        riot_champion_list = {}
        for champion in data:
            curr_info = data[champion]
            curr_key = champion
            riot_champion_list[curr_key] = {}
            riot_champion_list[curr_key]["name"] = curr_info["name"]
            riot_champion_list[curr_key]["id"] = curr_info["id"]
            riot_champion_list[curr_key]["title"] = curr_info["title"]

        sql = """
            SELECT
                "key"
            FROM
                "champion"
            """

        # the query returns an array such that array[0][0]
        # is the actual champion key
        temp_champion_list = Db.query(sql)
        local_champion_list = []

        for key in temp_champion_list:
            local_champion_list.append(key[0])

        key_diff = []

        # list the champions that haven't been updated
        for key in riot_champion_list:
            if key not in local_champion_list:
                key_diff.append(key)

        iter_total = len(key_diff)
        iter_curr = 1

        for key in key_diff:
            curr_champ = data[key]

            sql = """
                INSERT INTO
                    'champion' (key, name, id, title)
                VALUES
                    (:key, :name, :id, :title)
                """
            params = {
                "key": key,
                "name": curr_champ["name"],
                "id": curr_champ["id"],
                "title": curr_champ["title"]
            }

            Db.query(sql, params)

            print("Updated ",
                  iter_curr, "/",
                  iter_total,
                  " champions updated.")
            iter_curr += 1

    def get_account_data(self) -> str:
        """
        Get account information for a user.

        Args:
            self.username

        Returns:
            account_data: dictionary with account data

        """
        data = self.get_data_from_url("summoner/v3/summoners/by-name/" +
                                      self.username)

        return data


###############################################################################
# INITIALIZATION METHODS OVER
###############################################################################

    def get_champion_mastery(self) -> Dict[Any, Any]:
        """
        Return all data related to champion mastery.

        Args:
            self.account_data["id"]

        Returns:
            mastery_data - a dict with key champion ID

        """
        data = self.get_data_from_url(
            "champion-mastery/v3/champion-masteries/by-summoner/" +
            str(self.account_data["id"]))

        # data given is not ordered by key, unfortunately
        mastery_data = {}  # type: Dict
        for champion in data:
            champion_id = champion["champion_id"]
            mastery_data[champion_id] = {}
            for stat in champion:
                # cut out stats we have already
                if not stat == "champion_id" or stat == "playerId":
                    mastery_data[champion_id][stat] = champion[stat]

        return mastery_data

    def get_rank_data(self) -> str:
        """
        Return all data related to the users current rank.

        Args:
            self.account_data["id"]

        Returns:
            rank_data - dict with information on ranked things

        """
        data = self.get_data_from_url("league/v3/positions/by-summoner/" +
                                      str(self.account_data["id"]))

        # this returns an array with one entry so just
        # return the dict in there

        return data[0]


class Db:
    """Handle db connections/ return query results."""

    def query(self,
              query: str="",
              params: Dict[str, str]={},
              db_name: str="league_data.db"):
        """
        Run a query (also open and close the connection).

        Args:
            query - the query
            params - a dict with the parameters for the query
            db_name - database location relative to data.py

        Returns:
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
