# lfm_vis

Use the last.fm api to analyse listening patterns.

# Requirements

* Python 3.6
* pip

# Instructions

## Setting up the virtual environment

Navigate to the root folder.

### Linux

Only tested on Ubuntu

    python3.6 -m venv venv
    source venv/bin/activate
    python3.6 -m pip install -r requirements.txt

### Windows

Only tested in Powershell 6.0

    python -m venv venv
    .\venv\Script\activate
    python -m pip install -r .\requirements.txt

## Starting the flask server

### Ubuntu

    source venv/bin/activate
    cd lfm_vis
    python -m main
    
### Windows

    .\venv\Scripts\activate
    cd .\lfm_vis\
    python -m main