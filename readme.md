#Bones

Bones is a work-in-progress template for setting up a Flask project.  It uses [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap) , [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate), with [Flask-Testing](https://github.com/jarus/flask-testing), [nose](http://nose.readthedocs.org/en/latest/) and [tdaemon](https://github.com/brunobord/tdaemon) for testing.

##Setup

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

##Structure

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

###Root Directory

The root directory holds the myapp directory, tests directory, and, when the app is initialized per above instructions, the migrations directory.  The `run.py` file imports the myapp package and runs the server.

###`___init___.py`

The bulk of the Flask app is in the myapp package.  The myapp directory has an `___init___.py` file that imports the database, models, and views, and has the `create_app()` function.  When the myapp package is first imported, the `create_app()` function gets called and an app is created.  Inside that function the app is associated with the database `db` , and the views are registered to the app.

###`models.py`

SQLAlchemy models.  The example model is `Things`.  `models.py` also holds the database object, `db`, as well as a generic `get_or_create()` function that takes the `db` object, a model, and a keyword args dictionary, checks if the object in question has been created yet, if it has returns it, if not creates and returns it.  When you call `get_or_create()` the function signature for a "Thing" named "thing1" should look like:

~~~python

models.get_or_create(db, Things, **{"name":"thing1"})
~~~

i.e. don't forget to include the `**` operator before the dictionary.

###Views

Views are held in two different modules: `myapp/web/views_web.py` and 'myapp/api/views_api.py'.  Both are [pluggable views](http://flask.pocoo.org/docs/views/).

####API Views

The base class `APIView` is a pluggable view and so inherits from `MethodView`.  It handles GET and POST requests.

The `ThingsAPIView` class inherits from `APIView`.  Like all the classes that inherit from `APIView`, needs to implement `get_model_names`, `get_input_dict`, `create_items`, and `get_items` methods.  GET requests return JSON.  The docstring contains a `curl` statement that tests `ThingsAPIView` with a generic POST request.

####Web Views

Handles web page views.  Straightforward.  Base class is `ListView`.  Classes that inherit from `ListView`, as you might expect, display a collection of objects as a list.

####Registering Views







