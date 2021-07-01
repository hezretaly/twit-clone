from flask import Flask, request, current_app
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


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()
mail = Mail()
babel = Babel()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	moment.init_app(app)
	mail.init_app(app)
	babel.init_app(app)


	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.stats import bp as stats_bp
	app.register_blueprint(stats_bp, url_prefix='/stats')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)


	app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
			if app.config['ELASTICSEARCH_URL'] else None

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

	return app


# Translation happens based on language preferences of the user
@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models