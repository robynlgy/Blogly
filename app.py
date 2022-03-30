"""Blogly application."""

from email.mime import image
from urllib import response
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://davidjeffers:1234@localhost:5432/blogly' # added davidjeffers:1234@localhost:5432
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get('/')
def get_homepage():
    
    return redirect('/users')

@app.get('/users')
def get_users():

    users = User.query.all()

    return render_template("index.html", users=users)

@app.get('/users/new')
def get_new_user_page():

    return render_template("newUser.html")

@app.post('/users/new')
def post_new_user():
    
    first_name  = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


