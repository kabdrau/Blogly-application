"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

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

### Part1 ###

#List all users
# @app.route("/")
# def root():
#     """Redirect to list of users."""
#     return redirect("/users")

@app.route("/users")
def list_users():
    """List users."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)

# Add new user
@app.route("/users/new")
def add_user_form():
    """Show add user form"""
    
    return render_template("new-user.html")

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
    flash(f'User {user.get_full_name()} was added.', 'success')

    return redirect(f"/users/{user.id}")

# Show single user
@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.id).all()
    return render_template("show-user.html", user=user, posts=posts)

# Edit user
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Edit user form."""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

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
    flash(f'User {user.get_full_name()} was edited.', 'success')

    return redirect(f"/users/{user.id}")

# Delete user
@app.route("/users/<int:user_id>/delete", methods=["GET","POST"])
def delete_user(user_id):
    """Delete user and redirect to list all users."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.get_full_name()} was deleted.', 'error')

    return redirect("/users")

### Part2 ###

# Add new post
@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """Show add post form"""

    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add post and redirect to user details."""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    flash(f'Post {post.title} was added.', 'success')

    return redirect(f"/users/{user_id}")

# Show single post
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info on a single user."""

    post = Post.query.get(post_id)
    return render_template("show-post.html", post=post)

# Edit post
@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Edit post form."""

    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit post and redirect to post details."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f'Post {post.title} was edited.', 'success')

    return redirect(f"/posts/{post_id}")

# Delete post
@app.route("/posts/<int:post_id>/delete", methods=["GET","POST"])
def delete_post(post_id):
    """Delete user and redirect to list all users."""

    user_id = Post.query.get_or_404(post_id).users.id
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} was deleted.', 'error')

    return redirect(f"/users/{user_id}")

@app.route("/posts")
def list_posts():
    """List all posts."""

    posts = Post.query.order_by(Post.created_at).all()
    return render_template("posts.html", posts=posts)

@app.route("/")
def root():
    """List five posts."""

    msg = "5 latest"
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template("posts.html", posts=posts, msg = msg)