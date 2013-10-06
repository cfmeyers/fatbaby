Bones
=====

Bones is a work-in-progress template for setting up a Flask project.

Setup
-----
After cloning, get everything started by opening up the python interpreter and typing

~~~.bsh
~/bones $  python run.py db init
~~~

This command creates the alembic migrations directory.
Next, to create the first migration, type

~~~.bsh
~/bones $  python run.py db migrate
~~~

Your SQLite database file, `myapp.db`, will get created by that command.
Next, to upgrade type

~~~.bsh
~/bones $  python run.py db upgrade
~~~

And finally, to start the server,

~~~.bsh
~/bones $  python run.py runserver
~~~




