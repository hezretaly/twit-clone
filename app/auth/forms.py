from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
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

class ChangePasswordForm(FlaskForm):
	password = PasswordField(_l('Current Password'), validators=[DataRequired()])
	password_new = PasswordField(_l('New Password'), validators=[DataRequired()])
	password_new2 = PasswordField(_l('Repeat New Password'),
		validators=[DataRequired(), EqualTo('password_new', message=_l('Passwords must match'))])
	submit = SubmitField(_l('Submit'))

class ResetPasswordRequestForm(FlaskForm):
	username = StringField(_l('Username or Email'), validators=[DataRequired()])
	submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'),
		validators=[DataRequired(), EqualTo('password', message=_l('Passwords should match'))])
	submit = SubmitField(_l('Reset Password'))