"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#List all users
@app.route("/")
def root():
    """Redirect to list of users."""
    
    return redirect("/users")

@app.route("/users")
def list_users():
    """List users."""
    
    users = User.query.all()
    return render_template("users.html", users=users)

# Add new user
@app.route("/users/new")
def add_user_form():
    """Show add form"""
    
    return render_template("new.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to user details."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

# Show single user
@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

# Edit user
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Edit user form."""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user and redirect to user details."""

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    if request.form['image_url']:
        user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

# Delete user
@app.route("/users/<int:user_id>/delete", methods=["GET","POST"])
def delete_user(user_id):
    """Delete user and redirect to list all users."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/")