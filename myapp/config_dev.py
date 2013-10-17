import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir, "myapp.db")
DEBUG = True
APIKEY = "mykey"

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

