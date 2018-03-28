from time import time
from typing import Any

from flask import render_template


def stats_render() -> Any:
    """Returns stats page.
    """
    return render_template("stats.html", timestamp=time())
