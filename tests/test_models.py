import sys, unittest
sys.path.append("../")

from tests import TestCase
from myapp import models
from myapp.models import db, Things


class TestThings(TestCase):

    def test_add_Thing_to_db(self):
       thing = models.Things("test")
       db.session.add(thing)
       db.session.commit()
       assert db.session.query(Things).filter(Things.name=="test").first()

    def test_delete_Thing_to_db(self):
       thing = models.Things("test")
       db.session.add(thing)
       db.session.commit()
       assert db.session.query(Things).filter(Things.name=="test").first()
       db.session.delete(thing)
       db.session.commit()
       assert not db.session.query(Things).filter(Things.name=="test").first()
