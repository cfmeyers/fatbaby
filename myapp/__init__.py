from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.migrate import Migrate

from myapp.api.views_api import ThingsAPIView
from myapp.web.views_web import ThingsWebView, IndexView, LoginView

import config
from myapp.models import db


def reg_view(app, view, endpoint, url, methods=["GET", "POST"]):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=methods)
    return app

def register_api_views(app):
    app = reg_view(app, ThingsAPIView, "things_api", "/api/v1/things")
    return app

def register_web_views(app):
    app = reg_view(app, LoginView,     "login",    "/login")
    app = reg_view(app, IndexView,     "/",        "/")
    app = reg_view(app, IndexView,     "index",    "/index")
    app = reg_view(app, ThingsWebView, "things",   "/things")
    return app

def create_app(config={}):
    app = Flask(__name__)
    app.config.from_object('myapp.config')
    app.config.update(config)
    db.init_app(app)
    app = register_web_views(app)
    app = register_api_views(app)
    Bootstrap(app)
    return app

app = create_app()
migrate = Migrate(app, models.db)