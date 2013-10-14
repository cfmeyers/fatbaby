import sys, unittest
sys.path.append("../")
from tests import TestCase
from myapp import models
from myapp.models import db, Things, User

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

class TestUser(TestCase):

    def add_User(self, name, password):
        user = User(name, password)
        db.session.add(user)
        db.session.commit()

    def test_add_User_to_db(self):
        self.add_User("test", "password")
        test = db.session.query(User).filter(User.name=="test").first()
        assert test.check_password("password")

    def test_bad_validate(self):
        from myapp.web.views_web import bad_validate
        self.add_User("test", "password")
        self.add_User("test2", "notpassword")
        assert bad_validate("test", "password")
        assert not bad_validate("test2", "password")
        assert bad_validate("test2", "notpassword")












