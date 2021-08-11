"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

DEFAULT_IMG = "https://www.freeiconspng.com/img/1688"

class User(db.Model):
    """user model for site"""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """User full_name"""
        return f"{self.first_name} {self.last_name}"



class Posts(db.Model):
    """Post on the Blog"""

    __tablename__ = "posts"

    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) #import datetime and set default to current date and time.
    user_id = db.Coulmn(db.Integer, db.ForeignKey('users.id'), nullable=False) #sets foreign key reference 

    @property
    def format_date(self):
        """formats the date and returns it"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

class PostTag(db.Model):
    """Allows tagging on a post"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag for adding to a post"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags") #through join Post to Tags through posts_tags
        

def connect_db(app):
    """connects this databse to the provided Flask app"""

    db.app = app
    db.init_app(app)