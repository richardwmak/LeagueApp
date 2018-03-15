# lfm_vis

Use the last.fm api to analyse listening patterns.


# Instructions
## Setting up the virtual environment
Navigate to the root folder.

### Ubuntu
    python3.6 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
### Windows
    python -m venv venv
    .\venv\Script\activate
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