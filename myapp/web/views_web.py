from flask import (render_template, flash, redirect,
                   views, session, url_for, request, g)
from myapp import models, config, forms
from myapp.models import lm, db, User
from flask.ext.login import (login_user, logout_user,
                            current_user, login_required)

def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

def bad_validate(name, password):
    user = db.session.query(User).filter(User.name==name).first()

    if user and user.check_password(password):
        return user

    return False

class IndexView(views.View):
    """IndexView"""

    methods = ["GET"]

    def dispatch_request(self):
        return render_template("index.html")

class LoginView(views.View):
    """IndexView"""
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))

        form = forms.LoginForm()

        if form.validate_on_submit():
            user = bad_validate(form.username.data, form.password.data)
            if user:
                login_user(user, form.remember_me.data)
                flash('Login requested for username="'
                      + form.username.data
                      + '", Login requested for password="'
                      + form.password.data
                      + '", remember_me='
                      + str(form.remember_me.data))

                return redirect('/index')
            else:
                flash('failed to authenticate')
                return redirect('/login')


        return render_template("login.html", form=form)

class LogoutView(views.View):
    """IndexView"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))

class ListView(views.View):
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




