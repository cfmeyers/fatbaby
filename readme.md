Bones
=====

Bones is a work-in-progress template for setting up a Flask project.  It uses [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap) , [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate), with [Flask-Testing](https://github.com/jarus/flask-testing), [nose](http://nose.readthedocs.org/en/latest/) and [tdaemon](https://github.com/brunobord/tdaemon) for testing.

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

Your SQLite database file, `bones/myapp/myapp.db`, will get created by that command.
Next, to upgrade type

~~~.bsh
~/bones $  python run.py db upgrade
~~~

And finally, to start the server,

~~~.bsh
~/bones $  python run.py runserver
~~~

Structure
=========
~~~.bash
├── LICENSE
├── myapp
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── views_api.py
│   ├── config.py
│   ├── models.py
│   ├── static/
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── things.html
│   └── web
│       ├── __init__.py
│       └── views_web.py
├── readme.md
├── requirements.txt
├── run.py
└── tests/
~~~

Root Directory
--------------

The root directory holds the myapp directory, tests directory, and, when the app is initialized per above instructions, the migrations directory.  The ```run.py``` file imports the myapp package and runs the server.

```___init___.py```.bash file
-----------------------------

The bulk of the Flask app is in the myapp package.  The myapp directory has an ```___init___.py```.bash file that imports the database, models, and views, and has the ```create_app()```.python function.  When the myapp package is first imported, the ```create_app()```.python function gets called and an app is created.  Inside that function the app is associated with the database ```db```.python , and the views are registered to the app.

```models.py```.python file
-----


