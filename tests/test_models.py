import sys, unittest
sys.path.append("../")
from tests import TestCase, add_item_to_db
from datetime import datetime, timedelta
from myapp import models, utils
from myapp.models import (db, User, DirtyDiapers, WetDiapers,
                          NapStarts, Wakings, Weighings, Feedings)
from myapp.api import views_api

def add_and_commit(item):
    db.session.add(item)
    db.session.commit()

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

class TestNaps(TestCase):
    def test_Naps_interval(self):
        now = datetime.now()
        start = models.NapStarts(time=now)
        newnow = datetime.now()
        wake = models.Wakings(time=newnow)
        nap = models.Naps(start, wake)
        assert nap.interval == newnow - now


    def test_get_starts(self):
        now = datetime.now()
        twoMinute = timedelta(minutes=2)
        starts = [add_item_to_db(db, models.NapStarts,time=now+i*twoMinute) \
                                                    for i in range(5)]
        for i, start in enumerate(starts[:-1]):
            stop = add_item_to_db(db, models.Wakings, time=(now+(2*i)*twoMinute))
            add_item_to_db(db, models.Naps, start=start, end=stop)


        naps = db.session.query(models.Naps).all()
        # print "Naps"
        # for nap in naps:
            # print nap, nap.start, nap.end
        starts_with_naps = [nap.start for nap in naps]

        # print "from the database"
        dbStarts = db.session.query(models.NapStarts).all()
        # for start in dbStarts:
        #     print start, start.nap

        # assert False
        testStarts = views_api.get_nap_starts(db)

        # print "test starts"
        for start in testStarts:
            assert start not in starts_with_naps





class TestWeights(TestCase):
    def test_set_weight(self):
        now = datetime.now()
        subject = models.Weighings(time=now)
        subject.set_weight(lbs=1, oz=4)
        assert subject.ounces==20







