"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn2.iconfinder.com/data/icons/avatars-99/62/avatar-370-456322-512.png"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,  primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = True)
    image_url = db.Column(db.String, default = DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="users", cascade="all, delete-orphan")

    def get_full_name(self):
        """Get users full name."""
        if self.last_name == None:
            return self.first_name
        else:
            return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String, nullable = True)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def friendly_date(self):
        """Show date in a user friendly format"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")