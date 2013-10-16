import sys, os

INTERP = '/home/cfmeyers/.pythonbrew/venvs/Python-2.7.3/fl/bin/python'

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '/home/cfmeyers/.pythonbrew/venvs/Python-2.7.3/fl/bin')

sys.path.append(os.getcwd())

from testbaby.myapp import app as application
