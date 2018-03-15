# LeagueApp

This is intended to be a simple app that uses the Riot API
to download and parse data for a user and display it in a
way that looks good.

# Steps

1. Get the API to work.


# Instructions
## Setting up the virtual environment
Navigate to the root folder.

### Ubuntu
    python3.6 -m venv venv
    pip install -r requirements.txt
### Windows
    python -m venv venv
    pip install -r requirements.txt

## Starting the flask server

### Ubuntu
    source venv/bin/activate
    cd lfm_vis
    python -m main
    
### Windows
    .\venv\Scripts\activate
    cd .\lfm_vis\
    python -m main