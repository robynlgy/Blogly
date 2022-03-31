"""Blogly application."""

from email.mime import image
from urllib import response
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' # added davidjeffers:1234@localhost:5432
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def get_homepage():
    """Redirect to users page."""

    return redirect('/users')

@app.get('/users')
def get_users():
    """Show all users."""

    users = User.query.all()

    return render_template("index.html", users=users)

@app.get('/users/new')
def get_new_user_page():
    """Show new user form."""

    return render_template("newUser.html")

@app.post('/users/new')
def post_new_user():
    """Adding new user to database."""

    first_name  = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def get_user_detail(user_id):
    """Show user details page."""

    user = User.query.get(user_id)

    return render_template("userDetail.html",user=user)

@app.get('/users/<int:user_id>/edit')
def get_edit_form(user_id):
    """Show user edit page."""

    user = User.query.get(user_id)

    return render_template("editUser.html",user=user)

@app.post('/users/<int:user_id>/edit')
def post_edit_user(user_id):
    """Update user info in database."""

    first_name  = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def post_delete_user(user_id):
    """Delete user from database."""

    user = User.query.get(user_id)
    print("User..",user)
    User.query.filter(User.id==user_id).delete()
    db.session.commit()

    return redirect('/users')

