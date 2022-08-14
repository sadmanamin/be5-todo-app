import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'flask.db')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123456@localhost:5432/flask_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    # CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://"+CACHE_REDIS_HOST+":6379/0"
    CACHE_DEFAULT_TIMEOUT = 3300