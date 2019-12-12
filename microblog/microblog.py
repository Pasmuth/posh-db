from app import app, db, lists
from app.models import User, Post, Client, List, ListItem

@app.shell_context_processor
def make_shell_context():
	return {'db':db,
			'User':User, 
			'Post':Post, 
			'Client':Client, 
			'List':List, 
			'ListItem':ListItem,
			'Lists':lists}