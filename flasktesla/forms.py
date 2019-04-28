from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasktesla.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class RideForm(FlaskForm):
	date_of_ride = DateField('Date of Ride ', format='%Y-%m-%d', validators=[DataRequired()])
	start_lat = FloatField('Start Latitude' , validators=[DataRequired()])
	start_lng = FloatField('Start Longitude' , validators=[DataRequired()])
	end_lat = FloatField('End Latitude' , validators=[DataRequired()])
	end_lng = FloatField('End Longitude' , validators=[DataRequired()])
	avg_speed = IntegerField('Average Speed ' , validators=[DataRequired()])
	speed_limit = IntegerField('Speed Limit ' , validators=[DataRequired()])
	submit = SubmitField('Create Ride')

