# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~

    Define TestCase as base class for unit tests.
    Much code taken from
    https://github.com/imwilsonxu/fbone/blob/master/tests/__init__.py
"""

import sys, unittest, json
sys.path.append("../")

from flask.ext.testing import TestCase as Base
from myapp import create_app, db, models
from myapp.models import *

def add_item_to_db(db, model, **kwargs):
    item = get_or_create(db, model, **kwargs)
    db.session.add(item)
    db.session.commit()
    return item

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


# class HelpEventsAPIView(object):

#     PATH              = "/api/v1/"
#     JSON_HEADERS = {'Content-type': 'application/json'}

#     def get_endpoint(self, resourceName, fully_qualified=False):
#         return self.PATH+resourceName.lower()

#     def table_is_empty(self, client, url, resourceName):
#         response = client.get(url)
#         return not response.json[resourceName.lower()]

#     def POST_API(self):
#         url = self.get_endpoint(self.resource)
#         postJSON = json.dumps(self.postData)
#         response = self.client.post(url, data=postJSON, headers=self.JSON_HEADERS)

#         assert not self.table_is_empty(self.client, url, resource)



