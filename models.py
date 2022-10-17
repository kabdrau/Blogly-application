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

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.image_url} >"

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

    # posts_n_tags = db.relationship('PostTag', backref = 'post')

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at} {self.user_id} >"

    def friendly_date(self):
        """Show date in a user friendly format"""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag class."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50), nullable = False, unique = True)

    # tags_n_posts = db.relationship('PostTag', backref = 'tag')

    posts = db.relationship(
                'Post', 
                secondary = 'posts_tags', 
                backref = "tags",
                cascade="all, delete")

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

class PostTag(db.Model):
    """PostTag class."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key = True)

    def __repr__(self):
        return f"<PostTag {self.post_id} {self.tag_id}>"