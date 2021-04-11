import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	"""docstring for Config"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
	ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')
	MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH'))