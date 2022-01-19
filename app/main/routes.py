from flask import render_template, url_for, redirect, flash, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _
from datetime import datetime
import os
import uuid
import time
from app import db
from app.main.forms import  EditProfileForm, ImageUploadForm, EmptyForm, PostForm, ArticleForm, SearchForm
from app.models import User, Post, Article, Request
from app.main import bp


@bp.before_request
def before_request():
	# g.request_start=time.perf_counter()
	# g.request = Request(path=request.path, method=request.method, browser=request.user_agent.browser,
	# 				platform=request.user_agent.platform)
	if current_user.is_authenticated:
		# current_user.last_seen = datetime.utcnow()
		# db.session.commit()
		g.search_form = SearchForm()
		# g.request.user_id=current_user.id

# @bp.after_request
# def after_request(response):
# 	g.request.status_code=response.status_code
# 	g.request.response_time=time.perf_counter() - g.request_start
# 	db.session.add(g.request)
# 	db.session.commit()
# 	return response


@bp.route('/')
@bp.route('/index')
def index():
	return render_template('index.html', title='Home Page')

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	post_form = PostForm()
	if post_form.validate_on_submit():
		post = Post(body=post_form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(_('Your blog is now live'))
		return redirect(url_for('main.user', username=current_user.username))
	posts = user.posts.order_by(Post.timestamp.desc())
	form = EmptyForm()
	return render_template('user.html', user=user, form=form, post_form=post_form, \
		posts=posts)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes were saved'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@bp.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
	form = ImageUploadForm()
	if form.validate_on_submit():
		image = form.image.data
		filename = uuid.uuid4().hex + '.' + image.filename.rsplit('.',1)[1]
		if current_user.avatar_img is not None:
			file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', current_user.avatar_img)
			os.remove(file_path)
		current_user.avatar_img = filename
		image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', filename))
		db.session.commit()
		flash(_('Your image has been uploaded'))
		return redirect(url_for('main.user', username=current_user.username))
	return render_template('upload_image.html', title='Upload Avatar', form=form)

@bp.route('/delete_image', methods=['POST'])
@login_required
def delete_image():
	form = EmptyForm()
	if form.validate_on_submit():
		if current_user.avatar_img is None:
			flash(_('You do not have a custom avatar image'))
			return redirect(url_for('main.user', username=current_user.username))
		os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', current_user.avatar_img))
		current_user.avatar_img = None
		db.session.commit()
		flash(_('Your picture has been deleted'))
		return redirect(url_for('main.user', username=current_user.username))
	else:
		return redirect(url_for('main.index'))

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(_('User %(username)s not found', username=username))
			return redirect(url_for('main.index'))
		if user == current_user:
			flash(_('You cannot follow yourself!'))
			return redirect(url_for('main.user', username=username))
		current_user.follow(user)
		db.session.commit()
		flash(_('You are now following %(username)s!', username=username))
		return redirect(url_for('main.user', username=username))
	else:
		return redirect(url_for('main.index'))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash(_('User %(username)s not found', username=username))
			return redirect(url_for('main.index'))
		if user == current_user:
			flash(_('You cannot unfollow yourself!'))
			return redirect(url_for('main.user', username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash(_('You are now following %(username)s!', username=username))
		return redirect(url_for('main.user', username=username))
	else:
		return redirect(url_for('main.index'))

@bp.route('/explore')
@login_required
def explore():
	posts = Post.query.order_by(Post.timestamp.desc())
	return render_template('explore.html', title='Explore', posts=posts)

@bp.route('/my_feed')
@login_required
def my_feed():
	posts = current_user.followed_posts()
	return render_template('my_feed.html', title='Feed', posts=posts)

# articleList
@bp.route('/articles')
def articles():
	articles = Article.query.order_by(Article.timestamp.desc())
	return render_template('articles.html', title='Articles', articles=articles)

@bp.route('/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
	form = ArticleForm()
	if form.validate_on_submit():
		article = Article(header=form.header.data, body=form.body.data, author=current_user)
		db.session.add(article)
		db.session.commit()
		flash(_('Your article is now live!'))
		return redirect(url_for('main.articles'))
	return render_template('edit_article.html', title='Article', form=form)

# articleEdit
@bp.route('/edit_article/<int:id>', methods=['GET', 'POST'])
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

@bp.route('/article/<int:id>')
def article(id):
	article = Article.query.get_or_404(id)
	return render_template('article.html', title='Article', article=article)

@bp.route('/search')
@login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	posts, total = Post.search(g.search_form.q.data, 1, 10)
	return render_template('search.html', title=_('Search'), posts=posts)

@bp.route('/search_article')
@login_required
def search_article():
	if not g.search_form.validate():
		return redirect(url_for('main.articles'))
	articles, total = Article.search(g.search_form.q.data, 1, 10)
	return render_template('search.html', title=_('Search Articles'), articles=articles)