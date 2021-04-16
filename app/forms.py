from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password',
		validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different name')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email')

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)]) 
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

class ChangePasswordForm(FlaskForm):
	password = PasswordField('Current Password', validators=[DataRequired()])
	password_new = PasswordField('New Password', validators=[DataRequired()])
	password_new2 = PasswordField('Repeat New Password',
		validators=[DataRequired(), EqualTo('password_new', message='Passwords must match')])
	submit = SubmitField('Submit')

class ImageUploadForm(FlaskForm):
	image = FileField('Image', validators=[
		FileRequired(),
		FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
	])
	submit = SubmitField('Upload image')

class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')

class PostForm(FlaskForm):
	post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')

class ArticleForm(FlaskForm):
	header = StringField('Header', validators=[DataRequired()])
	body = TextAreaField('Main area', validators=[DataRequired(), Length(min=1, max=1024)])
	submit = SubmitField('Post')
