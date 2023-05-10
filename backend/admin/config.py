import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres_db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True