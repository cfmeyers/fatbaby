from flask.views import View, MethodView
from flask import render_template, request
from myapp import models
from myapp.models import db

class IndexView(View):
    """IndexView"""
    methods = ["GET"]

    def dispatch_request(self):
        return render_template("index.html")


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

