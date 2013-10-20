
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


