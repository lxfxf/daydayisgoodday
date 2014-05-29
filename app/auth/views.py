from flask import render_template
from ..models import User
from flask import flash, redirect, url_for, request
from forms import LoginForm
from . import auth
from flask.ext.login import login_user, logout_user, login_required

@auth.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			flash('Welcome, User!')
			return redirect(request.args.get('next') or url_for('main.index'))
		else:
			flash('Invalid username or password!')
			return redirect(url_for('auth.login'))

	return render_template('login.html',
		title = 'login',
		form = form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))