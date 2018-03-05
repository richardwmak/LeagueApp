"""
Handles the API requests and data storage.

Test commands:

from importlib import reload
import sys

if "data" in sys.modules:
    reload(data)
else:
    import data

data1 = data.ApiRequest("reeepicheeep", "EUW1")
"""

from   .db import Db
import configparser
import logging
import requests
from   typing import Tuple

# set up logging
logger = logging.getLogger(__name__)


class ApiRequest:
    """TODO: write docstring."""

###############################################################################
# INITIALIZATION METHODS
###############################################################################

    def __init__(self):
        """Get api key from ini.

        TODO: somehow do this in a sensible way when in prod
        """
        config = configparser.ConfigParser()
        config.read("secrets.ini")
        self.api_key = config["api"]["key"]
        self.version = None
        self.account_data = []

    def init_user(self, username: str, region: str):
        """Set user variables.

        Arguments:
            username {str} --
            region {str} --
        """
        self.username = username
        self.region = region

    def get_account_data(self) -> Tuple[str, int]:
        """Request account data based on username and region.

        Returns:
            Tuple[str, int] -- Tuple containing account data and the HTTP
                status code
        """
        (data, status_code) = self.get_data_from_url(
            "summoner/v3/summoners/by-name/" +
            self.username)

        return data, status_code

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

        # TODO: consider if I want to rerun depending on result
        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s" % e.reason)
            return False
        riot_version = data[0]

        if riot_version == local_version:
            # if the versions are the same, we can assume everything has
            # updated just fine
            logger.info("LeagueApp is up to date.")
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
                logger.info("Version could not be updated.")
                # TODO: raise exception
            else:
                logger.info("Version successfully updated.")

            self.update_champion()

    def get_data_from_url(self, url: str) -> Tuple[str, int]:
        """
        Get data from Riot API.

        It is always of the form

        https://REGION.api.riotgames.com/lol/API_CATEGORY?api_key=API_KEY

        Arguments:
            self.region --
            self.api_key --
            url -- location of the data (i.e. API_CATEGORY)

        Returns:
            Tuple[str, int] -- the decoded json data, HTML status code resp.
        """
        logger.info("Attempting to connect to Riot API.")
        complete_url = "https://%s.api.riotgames.com/lol/%s" % (self.region, url)
        headers = {"X-Riot-Token": self.api_key}
        logger.info("URL: %s" % complete_url)
        try:
            http_response = requests.get(
                complete_url,
                headers=headers)
            data = http_response.json()
            status_code = http_response.status_code

            if status_code is 200:
                logger.info("Successfully retrieved data.")
            else:
                logger.error("Failed to retrieve data. HTTP error code: %s" % status_code)

            return data, status_code

        except requests.HTTPError as e:
            logger.info("An HTTP error has occured: %s" % e)
            return None, 0

        except requests.Timeout as e:
            logger.info("Connection timed out: %s" % e)
            return None, 0

        except requests.RequestException as e:
            logger.info("Error processing HTTP request: %s" % e)
            return None, 0

    def update_champion(self):
        """
        Get champion names and IDs and puts them into the champion table.

        Args

        Returns

        """
        # the format of data is
        # data
        # |-- type: "champion"
        # |-- version: current version
        # |-- data
        #     |-- champion_first_data
        #     |-- ...
        #     |-- champion_last_data
        (data, status_code) = self.get_data_from_url(
            "static-data/v3/champions")["data"]

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


###############################################################################
# INITIALIZATION METHODS OVER
###############################################################################

    def get_champion_mastery(self):
        """
        Return all data related to champion mastery.

        Args
            self.account_data["id"]

        Returns
            mastery_data - a dict with key champion ID

        """
        (data, status_code) = self.get_data_from_url(
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

        Args
            self.account_data["id"]

        Returns
            rank_data - dict with information on ranked things

        """
        (data, status_code) = self.get_data_from_url(
            "league/v3/positions/by-summoner/" +
            str(self.account_data["id"]))

        # this returns an array with one entry so just
        # return the dict in there

        return data[0]
