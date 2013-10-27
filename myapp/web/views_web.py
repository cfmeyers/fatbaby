from flask import (render_template, flash, redirect,
                   views, session, url_for, request, g)
from myapp import models, forms, utils
from myapp.models import lm, db, Users
from flask.ext.login import (login_user, logout_user,
                            current_user, login_required)
from datetime import datetime

def before_request():
    g.user = current_user
    g.timeAsleep = utils.get_timedelta_dict(get_current_time_asleep())
    g.timeSinceLastSleep = utils.get_timedelta_dict(get_current_time_since_last_sleep())

def get_current_time_asleep():
    now = datetime.utcnow()
    napStarts = db.session.query(models.NapStarts).all()
    if napStarts:
        start = utils.get_most_recent_object(napStarts)
        if not start.nap:
            return now - start.time

    return None

def get_current_time_since_last_sleep():
    now = datetime.utcnow()
    if g.timeAsleep is None:
        naps = db.session.query(models.Naps).all()
        if naps:
            # mostRecentNap = utils.get_most_recent_object(naps)
            napEnds = [nap.end for nap in naps]
            napEnd = utils.get_most_recent_object(napEnds)
            return now - napEnd.time

    return None

@lm.user_loader
def load_user(id):
    return models.Users.query.get(int(id))

def validate(name, password):
    user = db.session.query(Users).filter(Users.name==name).first()

    if user and user.check_password(password):
        return user

    return False

class IndexView(views.View):
    """IndexView"""

    methods = ["GET"]

    def dispatch_request(self):
        if not current_user.is_authenticated():
            return redirect(url_for('login'))
        objects = utils.get_displayable_objects([models.Weighings,
                                                    models.Feedings,
                                                    models.BreastFeedings,
                                                    models.WetDiapers,
                                                    models.DirtyDiapers,
                                                    models.NapStarts,
                                                    models.Wakings], db)



        return render_template("index.html", objects=objects)

class LoginView(views.View):
    """Login View"""
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))

        form = forms.LoginForm()

        if form.validate_on_submit():
            user = validate(form.username.data, form.password.data)
            if user:
                login_user(user, form.remember_me.data)
                flash('Welcome, '+form.username.data)

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
        if not current_user.is_authenticated():
            return redirect(url_for('login'))
        context = {'objects':self.get_objects(),'title':self.get_title()}

        return self.render_template(context)


class ThingsWebView(ListView):
    def get_template_name(self): return "things.html"
    def get_objects(self): return models.Things.query.all()
    def get_title(self): return "Things"

class DirtyDiapersWebView(ListView):
    def get_template_name(self): return "diapers.html"
    def get_objects(self): return models.DirtyDiapers.query.all()
    def get_title(self): return "Dirty Diapers"

class WetDiapersWebView(ListView):
    def get_template_name(self): return "diapers.html"
    def get_objects(self): return models.WetDiapers.query.all()
    def get_title(self): return "Wet Diapers"

class FeedingsWebView(ListView):
    def get_template_name(self): return "feedings.html"
    def get_objects(self): return models.Feedings.query.all()
    def get_title(self): return "Feedings"

class BreastFeedingsWebView(ListView):
    def get_template_name(self): return "breastfeedings.html"
    def get_objects(self): return models.BreastFeedings.query.all()
    def get_title(self): return "Breast Feedings"

class NapsWebView(ListView):
    def get_template_name(self): return "naps.html"
    def get_objects(self):
        return sorted(models.Naps.query.all(), key=lambda x: x.end.time, reverse=True)
    def get_title(self): return "Naps"

class WeighingsWebView(ListView):
    def get_template_name(self): return "weighings.html"
    def get_objects(self): return models.Weighings.query.all()
    def get_title(self): return "Weight"

class RecordEventView(views.View):

    methods = ['GET', 'POST']

    def add_item_to_db(self, model, inputDict):
        item = model(**inputDict)
        db.session.add(item)
        db.session.commit()
        return item


    def dispatch_request(self):
        if not current_user.is_authenticated():
            return redirect(url_for('login'))

        form = forms.RecordEventForm()

        if request.method=='POST':
            if request.form['btn']=='Wet Diaper':
                self.add_item_to_db(models.WetDiapers, {"time":datetime.utcnow(), "user":g.user})
                return redirect(url_for('index'))

            if request.form['btn']=='Dirty Diaper':
                self.add_item_to_db(models.DirtyDiapers, {"time":datetime.utcnow(), "user":g.user})
                return redirect(url_for('index'))

            if request.form['btn']=='Fell Asleep':
                self.add_item_to_db(models.NapStarts, {"time":datetime.utcnow(), "user":g.user})
                return redirect(url_for('index'))

            if request.form['btn']=='Breast Fed':
                self.add_item_to_db(models.BreastFeedings, {"time":datetime.utcnow(), "user":g.user})
                return redirect(url_for('index'))

            if request.form['btn']=='feeding':
                try:
                    ounces = float(form.feeding.data)
                except:
                    return redirect(url_for('index'))
                if ounces:
                    self.add_item_to_db(models.Feedings, {"time":datetime.utcnow(), "user":g.user, "ounces": ounces})
                    return redirect(url_for('index'))


            if request.form['btn']=='weighing':
                total = 0.0
                pounds, ounces = None, None
                try:
                    pounds = float(form.weightPounds.data)
                except:
                    pass
                try:
                    ounces = float(form.weightOunces.data)
                except:
                    pass

                if pounds:
                    total += pounds * 16

                if ounces:
                    total += ounces
                self.add_item_to_db(models.Weighings, {"time":datetime.utcnow(), "user":g.user, "ounces": total})
                return redirect(url_for('index'))

            if request.form['btn']=='Woke Up':
                starts = utils.get_nap_starts(db, models.NapStarts)
                stop = self.add_item_to_db(models.Wakings, {"time":datetime.utcnow(), "user":g.user})
                nap = utils.build_nap(starts, stop, models.Naps)
                if nap:
                    db.session.add(nap)
                    db.session.commit()
                return redirect(url_for('index'))
            return "error"


        return render_template("record.html", form=form)











