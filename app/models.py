from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from datetime import datetime
from markdown import markdown
import bleach

class User(UserMixin, db.Model):
	__tablename__ = 'admins'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique = True, index = True)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	def __repr__(self):
		return '<User %r>' % self.username

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	body_html = db.Column(db.Text)
	comments = db.relationship('Comment', backref = 'post', lazy = 'dynamic')

	def __repr__(self):
		return '<Post %r>' % self.body

	@staticmethod
	def generate_fake(count = 100):
		from random import seed, randint
		import forgery_py

		seed()
		for i in xrange(count):
			p = Post(body = forgery_py.lorem_ipsum.sentences(randint(1, 3)),
				timestamp = forgery_py.date.date(True))
			db.session.add(p)
			db.session.commit()		
			
	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
        	markdown(value, output_format='html'),
        	tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)	

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	disabled = db.Column(db.Boolean)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	weibo_id = db.Column(db.Integer)