import requests
from bs4 import BeautifulSoup

def fetch_popular_films():
    page = requests.get('https://www.imdb.com/chart/moviemeter')
    soup = BeautifulSoup(page.text, 'html.parser')
    return [_parse_film(tr) for tr in soup.select('#main table.chart tbody tr')]


def _parse_film(tr):
    title = tr.select_one('td.titleColumn a').text
    year = tr.select_one('td.titleColumn span.secondaryInfo').text
    poster = tr.select_one('td.posterColumn img')['src']
    rating = tr.select_one('td.imdbRating').text
    imdbID = tr.select_one('td.ratingColumn div[data-titleid]')['data-titleid']
    return {
        'title': title,
        'year': year[1:5],
        'poster': fix_poster_url(poster, crop=True),
        'imdbRating': rating.strip(),
        'imdbID': imdbID
    }


def fix_poster_url(url, crop=False):
    path = 'https://images-na.ssl-images-amazon.com/images/'
    start_index = url.find('M')
    if not crop:
        size = ''
        end_index = len(url)
    else:
        size = '._V1_SX300_CR0,0,300,444_AL_.jpg'
        end_index = url.find('.', 48)
    return path + url[start_index:end_index] + size
