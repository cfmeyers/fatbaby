import sys
from datetime import datetime, timedelta
sys.path.append("../")
from myapp import models, utils

def test_match_waking_with_napstart():
    now = datetime.now()
    twoMinute = timedelta(minutes=2)
    starts = [models.NapStarts(time=now+i*twoMinute) for i in range(5)]
    stop =  models.Wakings(time=now+timedelta(minutes=3))
    match = utils.match_waking_with_napstart(starts, stop)

    for i, start in enumerate(starts):
        print i, start.time.strftime('%M:%S')
    print
    print "stop", stop.time.strftime('%M:%S')
    print "match", match.time.strftime('%M:%S')
    test = now+2*twoMinute
    print "assert", test.strftime('%M:%S')

    assert match.time == now+1*twoMinute

