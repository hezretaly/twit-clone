import os
# These are nesessary for loasing .env
# and os.getenv instead of environ.get
from dotenv import load_dotenv
load_dotenv()

class Config(object):
	"""docstring for Config"""
	SECRET_KEY = os.getenv('SECRET_KEY') or 'secret-key'

	# Database
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# File upload configuration
	UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
	ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
	MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))

	# Mail settings
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['a.hezret@outlook.com']

	# Languages
	LANGUAGES = ['en', 'zh']

	# Elasticsearch
	ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')