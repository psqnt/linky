import sqlite3
import click
import requests
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.exceptions import abort
from web_app.db import get_db


@click.command('crawl')
@with_appcontext
def crawl_command():
    """Clear the existing data and create new tables."""
    crawl()
    click.echo('crawled new links.')


def init_app(app):
    app.cli.add_command(crawl_command)


def make_request(url):
    print(url)
    response = requests.get(url)
    print(response.json())


def crawl():
    db = get_db()
    most_recent_link = db.execute(
        'SELECT * FROM links ORDER BY id DESC LIMIT 1'
    ).fetchone()
    print(most_recent_link)
    if most_recent_link is None:
        most_recent_link = 'http://joerogan.net'

    make_request(most_recent_link)
