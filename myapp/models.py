from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_or_create(db, model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance

########################################################################
class Things(db.Model):
    """"""
    __tablename__ = "things"

    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String)


    def __init__(self, name):
        """"""
        self.name = name.lower()

    def __repr__(self):
        if self.id:
            return '<Thing#%d: %s>' % (self.id, self.name)
        return '<Thing: %s>' % (self.name)

########################################################################