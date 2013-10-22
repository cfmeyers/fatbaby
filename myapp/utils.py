from collections import namedtuple
from datetime import datetime, timedelta
from pytz import timezone, utc
import pytz

EASTERN = pytz.timezone('US/Eastern')


def add_item_to_db(db, model, **kwargs):
    item = get_or_create(db, model, **kwargs)
    db.session.add(item)
    db.session.commit()
    return item

def match_waking_with_napstart(startsUnfiltered, stop):
    """Only send in starts that have not already been matched yet"""

    #ensure there are no start times greater than the stop time
    starts = [event for event in startsUnfiltered if event.time < stop.time]
    if starts:
        return min(starts, key=lambda x:abs(x.time-stop.time))
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
    Displayable = namedtuple('Displayable', 'type ounces time original')
    displayables = []
    for cl in classList:
        objects = get_todays_objects(cl, db)
        if cl.__name__ == 'Weighings' or cl.__name__ == 'Feedings':
            for object in objects:
                #create new datetime object that knows it's timezone is UTC
                utcAwareTime = utc.localize(object.time)
                estTime = utcAwareTime.astimezone(EASTERN)

                displayables.append(Displayable(type=cl.__name__, ounces=object.ounces, time=estTime, original=object))
        else:
            for object in objects:
                utcAwareTime = utc.localize(object.time)
                estTime = utcAwareTime.astimezone(EASTERN)
                displayables.append(Displayable(type=cl.__name__, ounces=None, time=estTime, original=object))

    return sorted(displayables, key=lambda x: x.time)









