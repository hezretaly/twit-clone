from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, login_required, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ChangePasswordForm
from app.models import User
from app.auth.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash(_('Invalid username or password'))
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('main.index'))
		return redirect(next_page)
	return render_template('auth/login.html', title='Sign in', form=form)

@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('You have been registered!'))
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title='Sign up', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if not current_user.check_password(form.password.data):
			flash(_('Wrong Password'))
			return redirect(url_for('auth.change_password'))
		current_user.set_password(form.password_new.data)
		db.session.commit()
		flash(_('Your password has been changed'))
		return redirect(url_for('auth.user', username=current_user.username))
	return render_template('auth/change_password.html', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.username.data).first() or \
			User.query.filter_by(username = form.username.data).first()
		if user:
			send_password_reset_email(user)
			flash(_('Check your E-mail for the instructions to reset your password'))
			return redirect(url_for('auth.login'))
		flash(_('Check if your information is correct'))
		return redirect(url_for('auth.reset_password_request'))
	return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_password_token(token)
	print(user)
	if not user:
		flash(_('Coud not find credentials'))
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_('Password has been reset.'))
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)