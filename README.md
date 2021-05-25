# Dynamic-Configuration-with-python
## Setup
For setting up the project run
* python3 -m venv venv
* pip install -r requirements.txt
## Development
### for windows: 
* set FLASK_APP=run.py
* flask run
### for linux:
* export FLASK_APP=run.py
* flask run
## Structure
* /app/ Contains the actual application
* .config/ Contains Flask and SCSS configuration.
* run.py Run to start Flask Server.
* data.db SQLite Database File.
