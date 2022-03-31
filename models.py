from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = 'https://i.guim.co.uk/img/media/fe1e34da640c5c56ed16f76ce6f994fa9343d09d/0_174_3408_2046/master/3408.jpg?width=700&quality=85&auto=format&fit=max&s=dfa532f0efa54ad2cda330f6d80f055c'

class User(db.Model):
    """Create user class and models table"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False
                     )
    last_name = db.Column(db.String(50),
                     nullable=False
                     )
    image_url = db.Column(db.String, nullable=False, default = DEFAULT_IMAGE_URL )

    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """Create post class and post table, connect post table to user table"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


