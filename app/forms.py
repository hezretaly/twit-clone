from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember me'))
	submit = SubmitField(_l('Sign in'))

class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'),
		validators=[DataRequired(), EqualTo('password', message=_l('Passwords must match'))])
	submit = SubmitField(_l('Register'))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_l('Please use a different name'))

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError(_l('Please use a different email'))

class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)]) 
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

class ChangePasswordForm(FlaskForm):
	password = PasswordField(_l('Current Password'), validators=[DataRequired()])
	password_new = PasswordField(_l('New Password'), validators=[DataRequired()])
	password_new2 = PasswordField(_l('Repeat New Password'),
		validators=[DataRequired(), EqualTo('password_new', message=_l('Passwords must match'))])
	submit = SubmitField(_l('Submit'))

class ImageUploadForm(FlaskForm):
	image = FileField(_l('Image'), validators=[
		FileRequired(),
		FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
	])
	submit = SubmitField(_l('Upload image'))

class EmptyForm(FlaskForm):
	submit = SubmitField(_l('Submit'))

class PostForm(FlaskForm):
	post = TextAreaField(_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField(_l('Submit'))

class ArticleForm(FlaskForm):
	header = StringField(_l('Header'), validators=[DataRequired()])
	body = TextAreaField(_l('Main area'), validators=[DataRequired(), Length(min=1, max=1024)])
	submit = SubmitField(_l('Post'))

class ResetPasswordRequestForm(FlaskForm):
	username = StringField(_l('Username or Email'), validators=[DataRequired()])
	submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'),
		validators=[DataRequired(), EqualTo('password', message=_l('Passwords should match'))])
	submit = SubmitField(_l('Reset Password'))