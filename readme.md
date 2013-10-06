Bones
=====

Bones is a work-in-progress template for setting up a Flask project.

Setup
-----
After cloning, get everything started by opening up the python interpreter and typing

~~~.python
python run.py db init
~~~

This command creates the alembic migrations directory.
Next, to create the first migration, type

~~~.bsh
python run.py db migrate
~~~

Then to upgrade type

~~~.bsh
python run.py db upgrade
~~~

And finally, to start the server,

~~~.bsh
python run.py runserver
~~~




