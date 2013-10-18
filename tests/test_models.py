import sys, unittest
sys.path.append("../")
from tests import TestCase
from datetime import datetime
from myapp import models
from myapp.models import (db, Things, User, DirtyDiapers, WetDiapers,
                          NapStarts, Wakings, Weighings, Feedings)

def add_and_commit(item):
    db.session.add(item)
    db.session.commit()

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
        return user

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

    def test_DirtyDiaper_User_Map(self):
        userTed = self.add_User("ted", "password")
        diaper = models.DirtyDiapers(time=datetime.now())
        diaper.user = userTed
        assert userTed.dirtydiapers

    def test_DirtyDiaper_User_Map(self):
        userTed = self.add_User("ted", "password")
        diaper = models.DirtyDiapers(time=datetime.now())
        diaper.user = userTed
        assert userTed.dirtydiapers

    def test_WetDiaper_User_Map(self):
        userTed = self.add_User("ted", "password")
        diaper = models.WetDiapers(time=datetime.now())
        diaper.user = userTed
        assert userTed.wetdiapers

    def test_NapStarts_User_Map(self):
        userTed = self.add_User("ted", "password")
        nap = models.NapStarts(time=datetime.now())
        nap.user = userTed
        assert userTed.napstarts

    def test_Wakings_User_Map(self):
        userTed = self.add_User("ted", "password")
        nap = models.Wakings(time=datetime.now())
        nap.user = userTed
        assert userTed.wakings

    def test_Weighings_User_Map(self):
        userTed = self.add_User("ted", "password")
        weighing = models.Weighings(time=datetime.now(), ounces=12)
        weighing.user = userTed
        assert userTed.weighings

    def test_Feedings_User_Map(self):
        userTed = self.add_User("ted", "password")
        feedings = models.Feedings(time=datetime.now(), ounces=12)
        feedings.user = userTed
        assert userTed.feedings

class TestWetDiapers(TestCase):
    def test_add_WetDiapers_to_db(self):
        now = datetime.now()
        diaper = models.WetDiapers(time=now)
        add_and_commit(diaper)
        assert db.session.query(WetDiapers).filter(WetDiapers.time==now).first()

    def test_waking_napstart(self):
        now = datetime.now()
        start = models.NapStarts(time=now)
        newnow = datetime.now()
        wake = models.Wakings(time=newnow)
        wake.set_start(start)
        assert wake.interval == newnow - now


class TestWeights(TestCase):
    def test_set_weight(self):
        now = datetime.now()
        subject = models.Weighings(time=now)
        subject.set_weight(lbs=1, oz=4)
        assert subject.ounces==20







