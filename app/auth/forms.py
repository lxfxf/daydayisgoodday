from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
	username = TextField('Username: ', validators = [Required()])
	password = PasswordField('Password: ', validators = [Required()])
	remember_me = BooleanField('Keep me logged in', default = False)
	submit = SubmitField('Log in')