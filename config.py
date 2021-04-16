import os
# These are nesessary for loasing .env
# and os.getenv instead of environ.get
from dotenv import load_dotenv
load_dotenv()

class Config(object):
	"""docstring for Config"""
	SECRET_KEY = os.getenv('SECRET_KEY') or 'secret-key'

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
	ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
	MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))