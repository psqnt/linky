import sqlite3
import click
import requests
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.exceptions import abort
from web_app.db import get_db


@click.command('crawl')
@click.argument('seed')
@with_appcontext
def crawl_command(seed):
    """Clear the existing data and create new tables."""
    main(seed)
    click.echo('Ran out of links to crawl.')


def init_app(app):
    app.cli.add_command(crawl_command)


def add_page_to_index(link, content):
    soup = BeautifulSoup(content, 'html.parser')
    try:
        title = soup.title.string.lower()
    except:
        title = "none"
    db = get_db()
    db.execute(
        'INSERT INTO websites (link, title) VALUES (?, ?)', (link, title)
    )
    db.commit()


def get_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        try:
            if 'http' in link.get('href'):
                links.append(link.get('href'))
        except Exception as e:
            pass
    return set(links)


def add_tocrawl(link):
    db = get_db()
    db.execute(
        'INSERT INTO tocrawl (link) VALUES (?)', (link,)
    )
    db.commit()


def get_seed():
    db = get_db()
    last_saved_website = db.execute(
        'SELECT link FROM tocrawl ORDER BY id DESC LIMIT 1'
    ).fetchone()
    return last_saved_website['link']


def in_database(url):
    db = get_db()
    website = db.execute(
        'SELECT link FROM websites WHERE link = (?)', (url,)
    ).fetchone()
    if website is None:
        return False
    return True


def union(a, b):
    for link in b:
        if link not in a:
            a.append(link)


def crawl(seed):
    """
    seed is a url
    """
    to_crawl = [seed]
    crawled = []
    index = []
    count = 0
    avoid = ['.zip', '.pdf', '.png', '.jpg', '.jpeg', '.doc', '.mp4', '.mov']
    while to_crawl and count < 100:
        url = to_crawl.pop()
        if 'facebook' not in url:
            if len(url) < 50:
                if url not in crawled:
                    if url[-4:] not in avoid:
                        if not in_database(url):
                            print(f'crawling: {url}')
                            try:
                                response = requests.get(url, timeout=20)
                            except Exception as e:
                                pass
                            content = response.content
                            add_page_to_index(url, content)
                            links = get_links(content)
                            union(to_crawl, links)
                            crawled.append(url)
                            #count += 1
        sleep(1)
    add_tocrawl(to_crawl[0])
    return crawled


def main(seed):
    if seed == 'restart':
        print('restarting from database')
        crawl(get_seed())
    else:
        crawl(seed)
