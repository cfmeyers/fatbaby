
from tests import TestCase
from models import Things


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
       db.session.delete(task)
       assert not db.session.query(Things).filter(Things.name=="test").first()
