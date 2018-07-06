import os

class Config:
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY', '')
    CACHE_POPULAR_FILMS_EXPIRE = 2 * 60 * 60
    CACHE_FILM_SEARCH_EXPIRE = 5 * 24 * 60 * 60
    CACHE_FILM_INFO_EXPIRE = 2 * 24 * 60 * 60


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379?db=0')


class ProductionConfig(Config):
    REDIS_URL = os.environ.get('REDIS_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
