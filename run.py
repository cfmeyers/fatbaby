from myapp import app
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__=="__main__":
    print app.config["SQLALCHEMY_DATABASE_URI"]
    manager.run()