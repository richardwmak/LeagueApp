"""Useful decorators (currently only one).
"""
import logging
from time import sleep
from typing import Callable


# set up logging
logger = logging.getLogger(__name__)


def retry(num_tries: int=3,
          time_between_tries: int=1,
          exception_to_check=BaseException):
    """Retry a function a certain amount of times, retrying if a certain exception is raised.

    Edited version of https://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Keyword Arguments:
        num_tries {int} -- (default: {3})
        time_between_tries {int} -- (default: {1})
        exception_to_check {Exception} -- Exception to check (default: {BaseException})
    """
    if num_tries <= 1:
        raise ValueError("Number of retries should be > 1.")

    if time_between_tries <= 0:
        raise ValueError("Time between tries should be non-zero.")

    def deco_retry(f: Callable):
        def f_retry(*args, **kwargs):
            total_tries = 0
            success = False
            while success is False and total_tries < num_tries:
                try:
                    return f(*args, **kwargs)
                except exception_to_check:
                    total_tries += 1
                    sleep(time_between_tries)
            # if we get here we failed
            return False
        return f_retry
    return deco_retry
