from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_babel import Babel
from elasticsearch import Elasticsearch


from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
mail = Mail(app)
babel = Babel(app)

if not app.debug:
	if app.config['MAIL_SERVER']:
		auth = None
		if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
			auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
		secure = None
		if app.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
			fromaddr='no-reply@' + app.config['MAIL_SERVER'],
			toaddrs=app.config['ADMINS'], subject='Microblog Failure',
			credentials=auth, secure=secure
		)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
		if app.config['ELASTICSEARCH_URL'] else None



@babel.localeselector
def get_locale():
	# return request.accept_languages.best_match(app.config['LANGUAGES'])
	return 'zh'


from app import routes, models, errors