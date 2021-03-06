from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models import User, Client
from app.lists import Lists

lists = Lists()

class LoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class CreatePost(FlaskForm):
	title = StringField('Title', validators = [DataRequired()])
	body = TextAreaField('Body', validators = [DataRequired()])
	submit = SubmitField('Publish')


class CreateClient(FlaskForm):
	gender_list_choices = list(zip(lists.genders.keys(), lists.genders.values()))
	race_choices = list(zip(lists.race.keys(), lists.race.values()))
	military_status = list(zip(lists.military.keys(), lists.military.values()))

	name = StringField('Name', validators = [DataRequired()])
	gender = SelectField('Gender', choices = gender_list_choices, coerce = int)
	race = SelectField('Race', choices = race_choices, coerce = int)
	military = SelectField('Military', choices = military_status, coerce = int)
	submit = SubmitField('Add Client')


class FilterClients(FlaskForm):
	gender_list_choices = list(zip(lists.genders.keys(), lists.genders.values()))
	race_choices = list(zip(lists.race.keys(), lists.race.values()))
	military_status = list(zip(lists.military.keys(), lists.military.values()))

	name = StringField('Name')
	gender = SelectField('Gender', choices = gender_list_choices, validators = [Optional()], coerce = int)
	race = SelectField('Race', choices = race_choices, validators = [Optional()], coerce = int)
	military = SelectField('Military', choices = military_status, validators = [Optional()], coerce = int)
	submit = SubmitField('Filter Results')


class AssessmentChooser(FlaskForm):
	client_list = list(zip([li.id for li in Client.query.all()],\
						   [li.name for li in Client.query.all()]))

	client = SelectField('Client', choices = client_list, coerce = int)
	submit = SubmitField('Submit')

class HousingAssessment(FlaskForm):
	housing_status_list = list(zip(lists.housing_status.keys(), lists.housing_status.values()))
	housing_status = SelectField('Housing Status', choices = housing_status_list, coerce = int)
	submit = SubmitField('Submit')


class FinancialAssessment(FlaskForm):
	total_income = IntegerField('Total Income')
	submit = SubmitField('Submit')