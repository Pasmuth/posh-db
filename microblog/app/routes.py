from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePost, CreateClient, FilterClients
from app.models import User, Post, Client
from app.lists import Lists

@app.route('/')
@app.route('/index')
@login_required
def index():
	posts = Post.query.filter_by(user_id = current_user.id)
	return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Now Registered')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form = form)


@app.route('/make_post', methods = ['GET', 'POST'])
@login_required
def make_post():
	form = CreatePost()
	if form.validate_on_submit():
		post = Post(title = form.title.data, body = form.body.data, user_id = current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('Post Published')
		return redirect(url_for('index'))
	return render_template('make_post.html', title = 'Create Post', form = form)

@app.route('/create_client', methods = ['GET', 'POST'])
@login_required
def create_client():
	form = CreateClient()
	if form.validate_on_submit():
		client = Client(name = form.name.data, 
			            gender = form.gender.data, 
			            race = form.race.data,
			            military = form.military.data,
			            created_by = current_user.id)
		db.session.add(client)
		db.session.commit()
		flash('Client Added')
		return redirect(url_for('view_clients'))
	return render_template('create_client.html', title = 'Create Client', form = form)


@app.route('/view_clients', methods = ['GET', 'POST'])
@login_required
def view_clients():
	lists = Lists()
	form = FilterClients()
	if form.validate_on_submit():
		clients = Client.query
		if form.name.data:
			clients = clients.filter(Client.name == form.name.data)
		if form.gender.data:
			clients = clients.filter(Client.gender == form.gender.data)
		if form.race.data:
			clients = clients.filter(Client.race == form.race.data)
		if form.military.data:
			clients = clients.filter(Client.military == form.military.data)
		clients = clients.all()
		return render_template('view_clients.html', title = 'Clients', clients = clients, lists = lists, form = form)
	clients = Client.query.all()
	return render_template('view_clients.html', title = 'Clients', clients = clients, lists = lists, form = form)