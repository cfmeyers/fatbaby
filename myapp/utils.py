from collections import namedtuple
from datetime import datetime, timedelta
from pytz import timezone, utc
import pytz

EASTERN = pytz.timezone('US/Eastern')
Displayable = namedtuple('Displayable', 'type pounds ounces time original')

def add_item_to_db(db, model, **kwargs):
    item = get_or_create(db, model, **kwargs)
    db.session.add(item)
    db.session.commit()
    return item

def get_most_recent_object(objects, now=None):
    """if using parameter now, ensure it's a UTC datetime object"""
    if now is None:
        now = datetime.utcnow()

    return min(objects, key=lambda x:abs(x.time-now))


def match_waking_with_napstart(startsUnfiltered, stop):
    """Only send in starts that have not already been matched yet"""

    #ensure there are no start times greater than the stop time
    if startsUnfiltered:
        starts = [event for event in startsUnfiltered if event.time < stop.time]
        if starts:
            return get_most_recent_object(starts)
    return None

def build_nap(starts, stop, Naps):

    matchedStart = match_waking_with_napstart(starts, stop)
    if matchedStart:
        nap = Naps(start=matchedStart, end=stop)
        return nap
    return None


def get_todays_objects(cl, db):
    """ Given a sqlalchemy table class, return a list of all rows whose date field >= today's date
        Args: cl:sqlalchemy table class
              db: reference to the database
        Returns: list of rows
    """
    today = datetime.today().strftime('%Y-%m-%d')
    return db.session.query(cl).filter(cl.time>today)

def get_displayable_objects(classList, db):
    displayables = []
    for cl in classList:
        objects = get_todays_objects(cl, db)
        if cl.__name__ == 'Weighings':
            for object in objects:
                estTime = get_date_in_EST(object.time)
                pounds = object.ounces // 16
                ounces = object.ounces - pounds * 16
                displayables.append(Displayable(type=cl.__name__,
                    pounds=int(pounds), ounces=int(ounces), time=estTime, original=object))

        if cl.__name__ == 'Feedings':
            for object in objects:
                estTime = get_date_in_EST(object.time)
                displayables.append(Displayable(type=cl.__name__, pounds=None, ounces=object.ounces, time=estTime, original=object))

        else:
            for object in objects:
                estTime = get_date_in_EST(object.time)
                displayables.append(Displayable(type=cl.__name__, pounds=None, ounces=None, time=estTime, original=object))

    return sorted(displayables, key=lambda x: x.time, reverse=True)


def get_date_in_EST(naiveUTCDate):
    #create new datetime object that knows it's timezone is UTC
    utcAwareTime = utc.localize(naiveUTCDate)
    return utcAwareTime.astimezone(EASTERN)


def get_timedelta_dict(delta):
    if delta != None:
        s = delta.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {"hours":hours, "minutes":minutes, "seconds":seconds}

    return None


def get_nap_starts(db, cl):
    """returns only the NapStarts rows that are not connected to a Nap"""
    return db.session.query(cl).filter(cl.nap==None).all()





