#Bones

Bones is a work-in-progress template for setting up a Flask project.  It uses

-  [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap)
-  [Flask-SQLAlchemy]()
-  [Flask-Login]()
-  [Flask-WTF]()
-  [Flask-Script]()
-  [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate)

####Testing

-  [Flask-Testing](https://github.com/jarus/flask-testing)
-  [nose](http://nose.readthedocs.org/en/latest/)
-  [tdaemon](https://github.com/brunobord/tdaemon)

##Setup

After cloning, get everything started by opening up the python interpreter and typing

~~~.bash
~/bones $  python run.py db init
~~~

This command creates the alembic migrations directory.
Next, to create the first migration, type

~~~.bash
~/bones $  python run.py db migrate
~~~

Your SQLite database file, `bones/myapp/myapp.db`, will get created by that command.
Next, to upgrade type

~~~.bash
~/bones $  python run.py db upgrade
~~~

All these steps can be executed in one fell swoop with the `init.sh` script:

~~~bash
~/bones $  bash init.sh
~~~

And finally, to start the server,

~~~.bash
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

##Testing

~~~bash
tdaemon -t nose --custom-args="--with-nosegrowlnotify -v"
~~~


####User Logins

Bones uses [Flask-Login]() to login users.  A user is modeled by the SQLAlchemy class `User`.  Per Flask-Login, the following methods have to be defined  for `User`:
~~~python

set_password(self, password)
check_password(self, password)
is_authenticated(self)
def is_active(self)
is_anonymous(self)
get_id(self)

~~~

For the reasons for each of these methods, see the [Flask-Login docs]().

All of the tutorials and examples for integrating Flask-Login into your app assume that you're not using an app-factory approach and you are using "app-defined" routes (e.g. `@app.route('/')`).  In order to facilitate my app-factory and pluggable views architecture I had to make some changes:

#####login manager

The examples I've run across instantiate the login manager object and also bind it to the app in the `__init__.py` file (after the app is created), much like the db object is for Flask-SQLAlchemy.

`__init__.py`
~~~python

from flask.ext.login import LoginManager
app = Flask(__name__)
lm = LoginManager(app)

~~~

This doesn't work with an app-factory approach.  Instead, I put the  "login manager" object in the `models.py` file.  I then imported it into the `__init__.py` file and bound it to the app inside of the `create_app()` function.


`__init__.py`
~~~python

from myapp.models import lm
def create_app(config={}):
    app = Flask(__name__)
    ...
    lm.init_app(app)
    ...
    return app

~~~

`models.py`
~~~python
from flask.ext.login import LoginManager
lm = LoginManager()
~~~

#####Decorated Flask-Login methods (with pluggable views)

Since I've got pluggable views, I didn't think I could decorate a method with the `@lm.load_user` method.  I was wrong.  No problem with that, so long as you instantiate the `lm` (login manager) object before you call the view or function that's been decorated with @lm.  I put my `user_loader()` function in my `views_web.py` module.

#####before_request()

In order to have access to the current user at all times, I created a `before_request()` function that runs before each request (ala [Michael Gruenberg's megaflask tutorial]()).  I then imported that function from `views_web.py` into `__init__.py` and decorated with Flask's `before_request` decorator:

~~~python
...
app = create_app()
app.before_request(before_request)
...

~~~

I can now access the g.user variable even in templates.

##API Key

Implemented an API key in the `APIView` class of `views_api.py` module. At this time only works for POST.


##Inspired By

-  [Fbone](https://github.com/imwilsonxu/fbone)
-  [Miguel Gruenberg's Flask Mega-Tutorial]()
