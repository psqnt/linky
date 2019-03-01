from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from web_app.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    db = get_db()
    links = db.execute(
        'SELECT id, link, title FROM links'
    ).fetchall()
    return render_template('index/index.html', links=links)
