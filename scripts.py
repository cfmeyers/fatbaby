from flask.ext.script import Command
from myapp.models import db, Things, User

class AddUser(Command):
    "add admin user"

    def run(self):
        user = User("admin", "password")
        db.session.add(user)
        db.session.commit()

