# Linky Setup

Clone the git repo

`git clone repo`

Go into directory

`cd linky`

Create a python virutal environment

`python3 -m venv venv`

Activate virtual env

`. ./venv/bin/activate`

Install required python libraries

`pip install .`

Set Flask environment (web server path)

`export FLASK_APP=web_app`
`export FLASK_ENV=development`

Initialize the database

`flask init-db`

Start the server

`flask run`

the database will be empty so run the crawler to populate the database

`flask crawl seed`

example:

`flask crawl http://bitcoin.it/`
