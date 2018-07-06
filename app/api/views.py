import json
import requests
from flask import current_app, request, jsonify, abort
from .. import cache
from . import api
from .decorators import cross_origin
from .scrapers import fetch_popular_films, fix_poster_url

@api.route('/films/')
@cross_origin()
def get_films():
    key = 'popular_films'
    if cache.exists(key):
        popular_films = json.loads(cache.get(key))
    else:
        popular_films = fetch_popular_films()
        cache.set(key, json.dumps(popular_films), ex=current_app.config['CACHE_POPULAR_FILMS_EXPIRE'])
    return jsonify(popular_films)


_OMDB = 'http://www.omdbapi.com/?apikey=' + current_app.config['OMDB_API_KEY']

@api.route('/films/search')
@cross_origin()
def search_films():
    title = request.args.get('title', '')
    key = f'search:{title}'
    if cache.exists(key):
        films = json.loads(cache.get(key))
    else:
        page = requests.get(f'{_OMDB}&s={title}&type=movie')
        films = page.json()
        if films.get('Response') == 'True':
            for film in films.get('Search'):
                if film.get('Poster')[8:10] == 'ia':
                    film['Poster'] = fix_poster_url(film['Poster'])
        cache.set(key, json.dumps(films), ex=current_app.config['CACHE_FILM_SEARCH_EXPIRE'])
    return jsonify(films)


@api.route('/films/<film_id>')
@cross_origin()
def get_film(film_id):
    key = f'film:{film_id}'
    if cache.exists(key):
        film = json.loads(cache.get(key))
    else:
        try:
            page = requests.get(f'{_OMDB}&i={film_id}&plot=full', timeout=10)
        except requests.exceptions.Timeout:
            abort(500)
        film = page.json()
        if not film.get('Response') == 'True':
            abort(404)
        if film.get('Poster')[8:10] == 'ia':
            film['Poster'] = fix_poster_url(film['Poster'])
        cache.set(key, json.dumps(film), ex=current_app.config['CACHE_FILM_INFO_EXPIRE'])
    return jsonify(film)
