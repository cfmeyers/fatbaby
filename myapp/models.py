from datetime import datetime, timedelta
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from pytz import timezone, utc
import pytz

EASTERN = pytz.timezone('US/Eastern')
ROLE_USER = 0
ROLE_ADMIN = 1

EST_UTC_TIME_DIFF = timedelta(hours=4)


db = SQLAlchemy()
lm = LoginManager()

def get_or_create(db, model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance

def get_date_in_EST(naiveUTCDate):
    utcAwareTime = utc.localize(naiveUTCDate)
    return utcAwareTime.astimezone(EASTERN)

########################################################################
class Weighings(db.Model):
    """"""
    __tablename__ = "weighings"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    ounces = db.Column(db.Float)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('weighings', order_by=id))

    def set_weight(self, oz=0.0, lbs=0.0):
        self.ounces = lbs*16 + oz

    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)

########################################################################
class Feedings(db.Model):
    """"""
    __tablename__ = "feedings"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    ounces = db.Column(db.Float)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('feedings', order_by=id))

    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)


########################################################################
class BreastFeedings(db.Model):
    """"""

    __tablename__ = "breastfeedings"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('breastfeedings', order_by=id))

    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)
########################################################################

class WetDiapers(db.Model):
    """"""
    __tablename__ = "wetdiapers"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('wetdiapers', order_by=id))


    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)
########################################################################
class DirtyDiapers(db.Model):
    """"""
    __tablename__ = "dirtydiapers"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    magnitude = db.Column(db.Integer)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('dirtydiapers', order_by=id))

    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)
########################################################################
class NapStarts(db.Model):
    """"""
    __tablename__ = "napstarts"

    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    note = db.Column(db.Text)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('napstarts', order_by=id))


    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)


    def __repr__(self):
        return '<NapStart:'+self.time.strftime('%H:%M')+'>'


########################################################################
class Wakings(db.Model):
    """"""
    __tablename__ = "wakings"
    id   = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    note = db.Column(db.Text)



    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users",
                            backref=db.backref('wakings', order_by=id))


    def get_time_as_EST(self):
        if self.time:
            return get_date_in_EST(self.time)


    def __repr__(self):
        return '<Waking:'+self.time.strftime('%H:%M')+'>'
########################################################################
class Naps(db.Model):
    """"""
    __tablename__ = "naps"

    id   = db.Column(db.Integer, primary_key=True)
    interval = db.Column(db.Interval)

    napstart_id =db.Column(db.Integer, db.ForeignKey('napstarts.id'))
    start = db.relationship("NapStarts",
                            backref=db.backref('nap', order_by=id))

    waking_id =db.Column(db.Integer, db.ForeignKey('wakings.id'))
    end = db.relationship("Wakings",
                            backref=db.backref('nap', order_by=id))

    def get_interval_dict(self):
        if self.interval:
            s = self.interval.seconds
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            return {"hours":hours, "minutes":minutes, "seconds":seconds}

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.interval = end.time - start.time

    def __repr__(self):
        return '<Nap: '+str(self.interval.total_seconds()/60)+' min>'

########################################################################
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    pw_hash = db.Column(db.String(120))


    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        """Should return True unless the object represents a users that should not be allowed to authenticate for some reason. """
        return True

    def is_active(self):
        """should return True for users unless they are inactive (e.g. they've been banned)"""
        return True

    def is_anonymous(self):
        """should return True only for fake users that are not supposed to log in to the system."""
        return False

    def get_id(self):
        """should return a unique identifier for users, in unicode format. """
        return unicode(self.id)

    def __init__(self, name, password):
        """"""
        self.name = name
        self.pw_hash = generate_password_hash(password)

    def __repr__(self):
        return '<Users %r>' % (self.name)

