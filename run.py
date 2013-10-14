from myapp import app
import scripts
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('add-admin', scripts.AddUser())

if __name__=="__main__":
    print app.config["SQLALCHEMY_DATABASE_URI"]
    manager.run()