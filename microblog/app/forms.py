from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, List, ListItem
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
	gender = SelectField('Gender', choices = gender_list_choices)
	race = SelectField('Race', choices = race_choices)
	military = SelectField('Military', choices = military_status)
	submit = SubmitField('Add Client')


class ListItem(FlaskForm):
	list_item = StringField('List Item')


class CreateList(FlaskForm):
	list_name = StringField('List Name')
	list_items = FieldList(FormField(ListItem), min_entries = 2)
	submit = SubmitField('Create List')