import json
from threading import Timer
from flask import Blueprint, current_app
from .. import cache
from .scrapers import fetch_popular_films

api = Blueprint('api', __name__)

def interval_fetch(interval):
    timer = Timer(interval, interval_fetch, args=(interval,))
    timer.daemon = True
    timer.start()
    popular_films = fetch_popular_films()
    cache.set('popular_films', json.dumps(popular_films), ex=interval)

interval_fetch(current_app.config['CACHE_POPULAR_FILMS_EXPIRE'])

from . import views, errors
