from   flask import render_template
from   time import time


def login_render(auth_url: str):
    """Return login page.

    Arguments:
        auth_url {str} -- Link to last.fm authorization page.
    """
    return render_template("login.html",
                           auth_url=auth_url,
                           timestamp=time())
