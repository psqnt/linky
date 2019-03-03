from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from web_app.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():

    # if POST
    if request.method == 'POST':
        return results(request.form['search'])
    else:
        db = get_db()
        links = db.execute(
            'SELECT link, title FROM websites'
        ).fetchall()
        link = links[0]
        count = len(links)
        return render_template('index/index.html', link=link, count=count)


@bp.route('/all')
def index_all():
    db = get_db()
    results = db.execute(
        'SELECT link, title FROM websites'
    ).fetchall()
    return render_template('index/results.html', results=results)


@bp.route('/results')
def results(search):
    words = search.lower().split()
    db = get_db()
    results = []
    db_results = db.execute(
        'SELECT link, title FROM websites',
    ).fetchall()

    # brute FORCE!
    for word in words:
        for r in db_results:
            if word in r['title']:
                results.append(r)

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('index/results.html', results=results)
