from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, \
	ImageUploadForm
from app.models import User


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			return redirect(url_for('index'))
		return redirect(next_page)
	return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have been registered!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Sign up', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes were saved')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if not current_user.check_password(form.password.data):
			flash('Wrong Password')
			return redirect(url_for('change_password'))
		current_user.set_password(form.password_new.data)
		db.session.commit()
		flash('Your password has been changed')
		return redirect(url_for('user', username=current_user.username))
	return render_template('change_password.html', form=form)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
	form = ImageUploadForm()
	if form.validate_on_submit():
		image = form.image.data
		filename = uuid.uuid4().hex + '.' + image.filename.rsplit('.',1)[1]
		if current_user.avatar_img is not None:
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'avatars', current_user.avatar_img)
			os.remove(file_path)
		current_user.avatar_img = filename
		image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars', filename))
		db.session.commit()
		flash('Your image has been uploaded')
		return redirect(url_for('user', username=current_user.username))
	return render_template('upload_image.html', title='Upload Avatar', form=form)