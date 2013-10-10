from flask.views import View, MethodView
from flask import render_template, request, flash, redirect
from myapp import models
from myapp.forms import LoginForm
from myapp.models import db
from myapp import config

class IndexView(View):
    """IndexView"""
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("index.html")

class LoginView(View):
    """IndexView"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = LoginForm()

        ##validate_on_submit gathers all the data from submitted form,
        ##runs the validators on it, and if the data is valid returns true
        if form.validate_on_submit():

            ##creates a flash message
            flash('Login requested for OpenID="'
                                          + form.openid.data
                                          + '", remember_me='
                                          + str(form.remember_me.data))

            ##returns user to /index
            return redirect('/index')

        return render_template("login.html",
                                form=form,
                                providers = config.OPENID_PROVIDERS)


class ListView(View):
    """Generic ListView for a model"""
    methods = ["GET"]
    def get_template_name(self): raise NotImplementedError

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def dispatch_request(self):

        context = {'objects':self.get_objects(),'title':self.get_title()}

        return self.render_template(context)


class ThingsWebView(ListView):
    def get_template_name(self): return "things.html"
    def get_objects(self): return models.Things.query.all()
    def get_title(self): return "Things"

