from time import time
from typing import Any

from flask import render_template


def login_render(auth_url: str) -> Any:
    """Return login page.

    Arguments:
        auth_url {str} -- Link to last.fm authorization page.
    """
    return render_template("login.html", auth_url=auth_url, timestamp=time())
