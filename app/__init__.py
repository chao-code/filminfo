import os
import redis
from flask import Flask
from config import config

cache = None

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    global cache
    cache = redis.from_url(app.config['REDIS_URL'], decode_responses=True)

    with app.app_context():
        from .api import api
        app.register_blueprint(api, url_prefix='/api/v1')

    return app
