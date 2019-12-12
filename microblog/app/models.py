from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy ='dynamic')
	created_clients = db.relationship('Client', backref = 'intake completed by', lazy = 'dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)


class Client(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30))
	gender = db.Column(db.Integer)
	race = db.Column(db.Integer)
	military = db.Column(db.Integer)
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Client {}>'.format(self.name)