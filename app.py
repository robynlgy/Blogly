"""Blogly application."""

from email.mime import image
from urllib import response
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# debug = DebugToolbarExtension(app)
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

    users = User.query.order_by('last_name','first_name').all()

    return render_template("index.html", users=users)

@app.get('/users/new')
def get_new_user_page():
    """Show new user form."""

    return render_template("new_user.html")

@app.post('/users/new')
def post_new_user():
    """Adding new user to database."""

    first_name  = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash('New User added!')
    return redirect('/users')

@app.get('/users/<int:user_id>')
def get_user_detail(user_id):
    """Show user details page."""

    user = User.query.get_or_404(user_id)


    return render_template("user_detail.html",user=user)

@app.get('/users/<int:user_id>/edit')
def get_edit_form(user_id):
    """Show user edit page."""

    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html",user=user)

@app.post('/users/<int:user_id>/edit')
def post_edit_user(user_id):
    """Update user info in database."""

    first_name  = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    flash('User info updated.')
    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def post_delete_user(user_id):
    """Delete user from database."""

    user = User.query.get_or_404(user_id)

    # delete all posts created by user first - referential integrity
    for post in user.posts:
        db.session.delete(post)

    # print("User..",user)
    User.query.filter(User.id==user_id).delete()
    db.session.commit()

    flash('User deleted.')
    return redirect('/users')

# ========= BLOG POST ROUTES ==========

@app.get('/users/<int:user_id>/posts/new')
def get_post_form(user_id):
    """Show new post form"""

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)

@app.post('/users/<int:user_id>/posts/new')
def post_new_post(user_id):
    """Add user post to database"""

    title = request.form['title']
    content = request.form['content']
    # print('title', title)
    # print('content', content)
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash('Added new post')
    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def get_post(post_id):
    """Show a post"""

    post = Post.query.get_or_404(post_id)

    return render_template('show_post.html', post=post)

@app.get('/posts/<int:post_id>/edit')
def get_edit_post(post_id):
    """Show form to edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)

@app.post('/posts/<int:post_id>/edit')
def post_edit_post(post_id):
    """Update post in database"""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    flash('Post edited.')
    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def post_delete_post(post_id):
    """Delete post from database"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted.')
    return redirect(f'/users/{user_id}')