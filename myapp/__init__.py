from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.migrate import Migrate

from myapp.api.views_api import ThingsAPIView
from myapp.web.views_web import ThingsWebView, IndexView, LoginView, LogoutView, before_request

import config_dev
from myapp.models import db, lm, User


def reg_view(app, view, endpoint, url, methods=["GET", "POST"]):
    view.APIKEY = app.config['APIKEY']
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=methods)
    return app

def register_api_views(app):
    app = reg_view(app, ThingsAPIView, "things_api", "/api/v1/things")
    return app

def register_web_views(app):
    app = reg_view(app, LoginView,     "login",    "/login")
    app = reg_view(app, LogoutView,    "logout",   "/logout")
    app = reg_view(app, IndexView,     "/",        "/")
    app = reg_view(app, IndexView,     "index",    "/index")
    app = reg_view(app, ThingsWebView, "things",   "/things")
    return app


def create_app(config={}):
    app = Flask(__name__)
    app.config.from_object('myapp.config_dev')
    app.config.update(config)

    db.init_app(app)
    lm.init_app(app)
    # app.debug = True
    app = register_web_views(app)
    app = register_api_views(app)
    Bootstrap(app)

    return app
app = create_app()
app.before_request(before_request)
migrate = Migrate(app, models.db)
