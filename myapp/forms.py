from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, DecimalField
#Required is a wtf validator
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)



class RecordEventForm(Form):
    feeding = DecimalField('feeding')
    weightPounds = DecimalField('weightPounds')
    weightOunces = DecimalField('weightOunces')



