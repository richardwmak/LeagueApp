"""Handles the API requests and data storage

Test commands:

from importlib import reload
import sys

if "data" in sys.modules:
    reload(data)
else:
    import data

data1 = data.ApiRequest("reeepicheeep", "EUW1")
"""
import json
import logging
import sqlite3
from   urllib.request import urlopen
import urllib.error

# set up logging
logger = logging.getLogger(__name__)
if not __name__ == "__main__":
    # if not run from main, set up extra logging stuff
    logging.basicConfig(filename='LeagueApp.log', level=logging.INFO)
    
class ApiRequest:
    """"""
################################################################################
# INITIALIZATION METHODS
################################################################################

    def __init__(self, username, region):
        """
        Initializes various relevant variables (surprise, surprise)

        Args:
            username: League of Legends username
            region: Account region
        """

        self.api_key = "RGAPI-6a1c6e7c-367d-4d36-83b7-f754b9e1ee61"
        self.username = username
        self.region = region
        self.version = None

        # self.initialize_db()
        # set_version() both checks the version and run and get_champion_list()
        # if the version is different
        # self.set_version()

    
    def initialise_db(self):
        """
        Creates an empty database with all relevant tables if they don't exist
        """

        table_dict = {}
        table_dict['info'] = ['version TEXT PRIMARY KEY ASC']
        table_dict['champion'] = ['key INTEGER PRIMARY KEY', 'name TEXT']

################################################################################
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
################################################################################
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
################################################################################


    def update_league_version(self):
        """
        Check if the current league version matches the stored one
        """
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
        # https://ddragon.leagueoflegends.com/api/versions.json is a list of all
        # version with the first entry being the current version
        try:
            http_response = urlopen("https://ddragon.leagueoflegends.com/api/versions.json")
            http_content = http_response.read().decode("utf-8")
            data = json.loads(http_content)
        except urllib.error.URLError as e:
            print("An error has occured: " + e.reason)
        riot_version = data[0]

        if riot_version == local_version:
            # if the versions are the same, we can assume everything has updated
            # just fine
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

            if result == False:
                print("Version could not be updated.")
            else:
                print("Version successfully updated.")

            self.update_champion()


    def get_data_from_url(self, url):
        """
        Since data is pulled from Riot's API the same way
        basically every time, this function generalises it

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
            http_response = urlopen("https://" + self.region + ".api.riotgames.com/lol/" + url + "?api_key=" + self.api_key)
            http_content = http_response.read().decode("utf-8")
            data = json.loads(http_content)

            logger.info("Successfully retrieved data.")
            return data
        except urllib.error.URLError as e:
            logger.info("An error has occured: %s" % e.reason)

            return False


    def update_champion(self):
        """
        Method that gets champion names and IDs and puts them into the champion
        table

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

        values = []

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
            if not key in local_champion_list:
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

            print("Updated ", iter_curr, "/", iter_total, " champions updated.")
            iter_curr += 1


    def get_account_data(self):
        """
        Method to get account information for a user

        Args:
            self.username

        Returns:
            account_data: dictionary with account data
        """
        data = self.get_data_from_url("summoner/v3/summoners/by-name/"
            + self.username)

        return data


################################################################################
# INITIALIZATION METHODS OVER
################################################################################

    def get_champion_mastery(self):
        """
        Method that returns all data related to champion mastery

        Args:
            self.account_data["id"]

        Returns:
            mastery_data - a dict with key champion ID
        """

        data = self.get_data_from_url("champion-mastery/v3/champion-masteries/by-summoner/"
            + str(self.account_data["id"]))

        # data given is not ordered by key, unfortunately
        mastery_data = {}
        for champion in data:
            championId = champion["championId"]
            mastery_data[championId] = {}
            for stat in champion:
                # cut out stats we have already
                if not stat == "championId" or stat == "playerId":
                    mastery_data[championId][stat] = champion[stat]
        
        return mastery_data


    def get_rank_data(self):
        """
        Method that returns all data related to the users current rank

        Args:
            self.account_data["id"]

        Returns:
            rank_data - dict with information on ranked things
        """

        data = self.get_data_from_url("league/v3/positions/by-summoner/"
            + str(self.account_data["id"]))

        # this returns an array with one entry so just
        # return the dict in there

        return data[0]


class Db:
    """
    The database class that handles opening/closing db connections, and running
    and returning query results.
    """
    def query(query = "", params = {}, db_name="data/league_data.db"):
        """
        Run a query (also open and close the connection)

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
            conn = sqlite3.connect(db_name)
            conn.row_factory = dict_factory
            cursor = conn.cursor()

            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.commit()
            # close the connection
        except sqlite3.Error as e:
            logger.info("A database error has occurred: ", e.args[0])
            result = False
        finally:
            if not result == False:
                logger.info("Successfully ran query.")
            logger.info("Database connection closed.")
            conn.close()
            return result
