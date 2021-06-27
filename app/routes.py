from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, \
	ImageUploadForm, EmptyForm, PostForm, ArticleForm, ResetPasswordRequestForm, \
	ResetPasswordForm
from app.models import User, Post, Article
from app.email import send_password_reset_email


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/')
@app.route('/index')
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
			flash(_('Invalid username or password'))
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
		flash(_('You have been registered!'))
		return redirect(url_for('login'))
	return render_template('register.html', title='Sign up', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	post_form = PostForm()
	if post_form.validate_on_submit():
		post = Post(body=post_form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_('Your blog is now live'))
		return redirect(url_for('user', username=current_user.username))
	posts = user.posts.order_by(Post.timestamp.desc())
	form = EmptyForm()
	return render_template('user.html', user=user, form=form, post_form=post_form, \
		posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes were saved'))
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
			flash(_('Wrong Password'))
			return redirect(url_for('change_password'))
		current_user.set_password(form.password_new.data)
		db.session.commit()
		flash(_('Your password has been changed'))
		return redirect(url_for('user', username=current_user.username))
	return render_template('change_password.html', form=form)

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
		flash(_('Your image has been uploaded'))
		return redirect(url_for('user', username=current_user.username))
	return render_template('upload_image.html', title='Upload Avatar', form=form)

@app.route('/delete_image', methods=['POST'])
@login_required
def delete_image():
	form = EmptyForm()
	if form.validate_on_submit():
		if current_user.avatar_img is None:
			flash(_('You do not have a custom avatar image'))
			return redirect(url_for('user', username=current_user.username))
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars', current_user.avatar_img))
		current_user.avatar_img = None
		db.session.commit()
		flash(_('Your picture has been deleted'))
		return redirect(url_for('user', username=current_user.username))
	else:
		return redirect(url_for('index'))

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(_('User %(username)s not found', username=username))
			return redirect(url_for('index'))
		if user == current_user:
			flash(_('You cannot follow yourself!'))
			return redirect(url_for('user', username=username))
		current_user.follow(user)
		db.session.commit()
		flash(_('You are now following %(username)s!', username=username))
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(_('User %(username)s not found', username=username))
			return redirect(url_for('index'))
		if user == current_user:
			flash(_('You cannot unfollow yourself!'))
			return redirect(url_for('user', username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash(_('You are now following %(username)s!', username=username))
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
	posts = Post.query.order_by(Post.timestamp.desc())
	return render_template('explore.html', title='Explore', posts=posts)

@app.route('/my_feed')
@login_required
def my_feed():
	posts = current_user.followed_posts()
	return render_template('my_feed.html', title='Feed', posts=posts)

# articleList
@app.route('/articles')
def articles():
	articles = Article.query.order_by(Article.timestamp.desc())
	return render_template('articles.html', title='Articles', articles=articles)

@app.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
	form = ArticleForm()
	if form.validate_on_submit():
		article = Article(header=form.header.data, body=form.body.data, author=current_user)
		db.session.add(article)
		db.session.commit()
		flash(_('Your article is now live!'))
		return redirect(url_for('articles'))
	return render_template('edit_article.html', title='Article', form=form)

# articleEdit
@app.route('/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
	article = Article.query.get_or_404(id)
	form = ArticleForm()
	if form.validate_on_submit():
		article.header = form.header.data
		article.body = form.body.data
		db.session.commit()
	elif request.method == 'GET':
		form.header.data = article.header
		form.body.data = article.body
	return render_template('edit_article.html', title='Edit Article', form=form)

@app.route('/article/<int:id>')
def article(id):
	article = Article.query.get_or_404(id)
	return render_template('article.html', title='Article', article=article)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.username.data).first() or \
			User.query.filter_by(username = form.username.data).first()
		if user:
			send_password_reset_email(user)
			flash(_('Check your E-mail for the instructions to reset your password'))
			return redirect(url_for('login'))
		flash(_('Check if your information is correct'))
		return redirect(url_for('reset_password_request'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	print(user)
	if not user:
		flash(_('Coud not find credentials'))
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash(_('Password has been reset.'))
		return redirect(url_for('login'))
	return render_template('reset_password.html', form=form)

