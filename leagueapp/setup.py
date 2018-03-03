#!/usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "LeagueApp",
    version = "0.0.0",
    author = "Richard Mak",
    author_email = "richardwmak@gmail.com",
    description = ("Simple python app to parse and display league of legends stats"),
    license = "MIT",
    packages=['LeagueApp'],
    long_description=read('README.md')
    ],
)