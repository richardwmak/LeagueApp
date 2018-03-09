r"""
Controller.
"""
from   flask import Flask, redirect, request, url_for, render_template
from   model.auth import Auth
from   model.data import ApiRequest
import model.custom_session as custom_session
import logging
from   view.login import login_render


"""Initialise app."""
# Set up logging.
logger = logging.getLogger(__name__)

# Set up Flask app.
app = Flask(__name__,
            template_folder="../view/templates",
            static_folder="../view/static")
app.secret_key = ('\xd5\x99\x98N\x1e\xac7\xc9{\x9d\xdc\xefN\xdf\xcbR\xfc\x8f' +
                  '\xfa$\xa1\xa7\xd7j')


file_handler = logging.FileHandler(filename="app.log")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


# initialise session
session = custom_session.Session()
logger.info("Loaded session.")

# Create data object to use this session
api_request_instance = ApiRequest()
auth_instance = Auth()

# currently, the way to force a cache refresh to grab updated css files is to
# pass int(time.time()) and add that to the css file


@app.route("/")
def main_page():
    """Route to login or main screen."""
    if session.check_key("logged_in") and session.select_key("logged_in") is True:
        return redirect(url_for("stats"))
    else:
        return redirect(url_for("login"))


@app.route("/login")
def login(auth_instance: Auth = auth_instance):
    """Request user info."""
    auth_url = auth_instance.generate_auth_url()
    return login_render(auth_url=auth_url)


@app.route("/auth")
def auth_page():
    """Handle last.fm authorisation.
    """
    pass


@app.route("/set_info", methods=["GET"])
def set_info(api: ApiRequest = api_request_instance):
    """Get the token obtained from authorisation, then get the session key.

    Keyword Arguments:
        api {ApiRequest} -- (default: {api_request_instance})
    """
    # set the token
    new_token = request.args.get("token")
    auth_instance.get_session_key(new_token,
                                  api_request_instance,
                                  session)

    return redirect(url_for("stats"))


@app.route("/stats")
def stats():
    """Load main page."""
    return render_template("stats.html")


def start_server():
    """Start the Flask server.
    """
    logger.info("Flask app started up.")
    app.run(debug=True, port=5000)
