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
from urllib.request import urlopen
import urllib.error
import sqlite3

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
        self.api_key = "RGAPI-39eaf651-3b99-4822-9b04-7358d913652e"
        self.username = username
        self.region = region
        self.version = None

        self.champion_to_id = self.get_champion_list()

        # https://stackoverflow.com/questions/483666/python-reverse-invert-a-mapping
        # the following inverts the dictionary so we can
        # look up champion names by key
        self.id_to_champion = dict([ (v, k) for k, v in self.champion_to_id.items()])

        self.account_data = self.get_account_data()


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
        try:
            http_response = urlopen("https://" + self.region + ".api.riotgames.com/lol/" + url + "?api_key=" + self.api_key)
            http_content = http_response.read().decode("utf-8")
            data = json.loads(http_content)

            return data
        except urllib.error.URLError as e:
            print("An error has occured: " + e.reason)

            return False


    def get_champion_list(self):
        """
        Method that returns champions names and IDs.
        This is static so we can run it each time without issue

        Args:

        Returns:
            champion_list: dictionary of the form champion name => champion id
        """
        # the format of data is
        # data
        # |-- type: "champion"
        # |-- version: current version
        # |-- data
        #     |-- champion_first_data
        #     |-- ...
        #     |-- champion_last_data
        data = self.get_data_from_url("static-data/v3/champions")

        champion_list = {}
        for champion in data["data"]:
            champion_list[champion] = data["data"][champion]["id"]

        # while we're at it, set the current version
        self.version = data["version"]

        return champion_list


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


class DbMethods:
    """"""

    def __init__(self):
        self.db_name = "league_data"

    def query(self, sql, access_type):
        """
        Given a query, run it through sqlite3

        args:
            sql: the sql query
            access_type: either "read" or "write" depending on whether the sql
                query will affect the database

        return:

        """
        try:    
            with sqlite3.connect("data/league_data.db") as conn:
                cursor = conn.cursor()
                cursor.execute(sql)

                if access_type == "read":
                    return cursor.fetchall()
                elif access_type == "write":
                    conn.commit()
                    return True
        except sqlite3.Error as e:
            print("An error has occurred: ", e.args[0])
            return False