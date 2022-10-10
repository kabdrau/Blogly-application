"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                    nullable = False)
    last_name = db.Column(db.String(50),
                    nullable = True)
    image_url = db.Column(db.String, 
                    default = "https://cdn2.iconfinder.com/data/icons/avatars-99/62/avatar-370-456322-512.png")

    def get_full_name(self):
        """Get users full name."""
        if self.last_name == None:
            return self.first_name
        else:
            return f"{self.first_name} {self.last_name}"