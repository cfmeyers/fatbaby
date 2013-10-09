# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Much code taken from
    https://github.com/imwilsonxu/fbone/blob/master/tests/__init__.py
"""

import sys, unittest
sys.path.append("../")

from flask.ext.testing import TestCase as Base
from myapp import create_app, db, models
from myapp.models import *

class TestCase(Base):
    """Base TestClass for your application."""

    #in memory sqlite db
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        configs = {"SQLALCHEMY_DATABASE_URI":self.SQLALCHEMY_DATABASE_URI, "TESTING":self.TESTING}

        return create_app(configs)

    def setUp(self):
        self.app = self.create_app()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()







