from flask.ext.wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import Required
from flask.ext.pagedown.fields import PageDownField

class PostForm(Form):
	body = PageDownField("What's on your mind?", validators = [Required()])
	submit = SubmitField('Submit')

class CommentForm(Form):
	body = StringField('', validators = [Required()])
	submit = SubmitField('Submit')