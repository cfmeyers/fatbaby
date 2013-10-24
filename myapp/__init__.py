from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask.ext.migrate import Migrate

from myapp.api.views_api import (DirtyDiapersAPIView,
                                WetDiapersAPIView, FeedingsAPIView,
                                WeighingsAPIView, NapStartsAPIView,
                                WakingsAPIView)

from myapp.web.views_web import (IndexView, LoginView,
                                LogoutView, before_request, DirtyDiapersWebView,
                                WetDiapersWebView, FeedingsWebView,
                                WeighingsWebView, NapsWebView, RecordEventView)

import config_dev
from myapp.models import db, lm, Users


def reg_view(app, view, endpoint, url, methods=["GET", "POST"]):
    view.APIKEY = app.config['APIKEY']
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=methods)
    return app

def register_api_views(app):
    PATH = "/api/v1/"
    app = reg_view(app, DirtyDiapersAPIView, "ddiapers_api", PATH+"dirtydiapers")
    app = reg_view(app, WetDiapersAPIView, "wdiapers_api", PATH+"wetdiapers")
    app = reg_view(app, FeedingsAPIView, "feedings_api", PATH+"feedings")
    app = reg_view(app, WeighingsAPIView, "weighings_api", PATH+"weighings")
    app = reg_view(app, NapStartsAPIView, "napstarts_api", PATH+"napstarts")
    app = reg_view(app, WakingsAPIView, "wakings_api", PATH+"wakings")
    return app

def register_web_views(app):
    app = reg_view(app, LoginView,     "login",    "/login")
    app = reg_view(app, LogoutView,    "logout",   "/logout")
    app = reg_view(app, IndexView,     "/",        "/")
    app = reg_view(app, IndexView,     "index",    "/index")
    app = reg_view(app, DirtyDiapersWebView, "dirtydiapers",   "/dirtydiapers")
    app = reg_view(app, WetDiapersWebView, "wetdiapers",   "/wetdiapers")
    app = reg_view(app, FeedingsWebView, "feedings",   "/feedings")
    app = reg_view(app, WeighingsWebView, "weighings",   "/weighings")
    app = reg_view(app, NapsWebView, "naps",   "/naps")
    app = reg_view(app, RecordEventView, "record",   "/record")
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
