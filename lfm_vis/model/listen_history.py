"""To run this.

from model.api import ApiRequest
from model.custom_session import Session
from model.listen_history import ListenHistory
a = ApiRequest()
s = Session()
l = ListenHistory(a, s)
l.get_basic_info()
l.test()
"""


import logging
from   model.api import ApiRequest
from   model.custom_session import Session
from   model.db import Db

logger = logging.getLogger(__name__)


class ListenHistory:
    """
    Handles downloading the users entire download history.

    Must:
        1. Download the user history, respecting the API limits.
        2. Save the history frequently.
        3. When interrupted, save the spot and start there again next time.
    """

    def __init__(self,
                 apirequest: ApiRequest,
                 session: Session) -> None:
        """Initialisation stuff.

        Arguments:
            apirequest {ApiRequest}
            session {Session}
        """
        self.apirequest = apirequest
        self.session = session
        self.db = Db()

        self.username = self.session.select_key("username")
        curr_page_key = "listen_history.current_page"
        if self.session.check_key(curr_page_key):
            self.current_page = self.session.select_key(curr_page_key)
        else:
            self.current_page = 1

    def generate_data(self):
        """Get the json dict for up to 200 songs.
        """
        param_dict = {"limit": 200,
                      "user": self.username,
                      "page": self.current_page,
                      "method": "user.getRecentTracks"}
        (self.result, self.status_code) = self.apirequest.get_data_from_url(param_dict=param_dict)
        if not self.status_code == 200:
            logger.error("Failed to download last.fm data.")
            raise Exception("Failed to download last.fm data.")

    def generate_query_params(self):
        """Given the result of the api query generate the params.
        """
        self.params = []
        for track in self.result["recenttracks"]["track"]:
            if "@attr" in track:
                # @attr will only be a key if the song is playing meaning the
                # date will also be messed up so skip it
                continue
            artist      = track["artist"]["#text"]
            artist_mbid = track["artist"]["mbid"]
            song        = track["name"]
            song_mbid   = track["mbid"]
            album       = track["album"]["#text"]
            album_mbid  = track["album"]["mbid"]
            url         = track["url"]
            for img in track["image"]:
                if img["size"] == "small":
                    img_s = img["#text"]
                elif img["size"] == "medium":
                    img_m = img["#text"]
                elif img["size"] == "large":
                    img_l = img["#text"]
                elif img["size"] == "extralarge":
                    img_xl = img["#text"]
                else:
                    raise KeyError("Image key not found.")
            date_uts  = track["date"]["uts"]
            date_text = track["date"]["#text"]

            self.params.append((artist, artist_mbid,
                                song, song_mbid,
                                album, album_mbid,
                                url,
                                img_s, img_m, img_l, img_xl,
                                date_uts, date_text))

    def store_data(self):
        """Run the query to store the data.
        """
        try:
            self.db.query("""
                          INSERT OR IGNORE INTO listen_history
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                          """,
                          self.params)
        except Exception as e:
            logger.error("Failed to store data.")
            raise Exception("Failed to store data.")

    def init_db(self):
        """Create the database if it doesn't exist already.
        """
        try:
            self.db.query("""
                          CREATE TABLE IF NOT EXISTS listen_history
                          (
                              artist TEXT,
                              artist_mbid TEXT,
                              song TEXT,
                              song_mbid TEXT,
                              album TEXT,
                              album_mbid,
                              url TEXT,
                              img_s TEXT,
                              img_m TEXT,
                              img_l TEXT,
                              img_xl TEXT,
                              date_uts UNIQUE INT,
                              date_text TEXT
                              PRIMARY KEY (artist, song, date_uts)
                          )
                          """)
        except Exception as e:
            logger.error("Failed to create table.")
            raise Exception("Failed to create table.")

    def return_progress(self) -> str:
        """Return percentage currently at.
        """
        return str((100 / self.total_pages) * self.current_page)

    def get_basic_info(self):
        """
        Figure out how much data is downloaded/left, etc.
        """
        param_dict = {"limit": 200,
                      "user": self.username,
                      "method": "user.getRecentTracks"}

        (data, response) = self.apirequest.get_data_from_url(param_dict=param_dict)

        self.total_pages = int(data["recenttracks"]["@attr"]["totalPages"])

    def store_current_page(self):
        """Things to be done when the download gets paused.
        """
        self.session.insert_key_value("listen_history.current_page", 1)

    def test(self):
        """Test the class.
        """
        self.init_db()
        print(self.total_pages)
        self.generate_data()
        self.generate_query_params()
        self.store_data()
