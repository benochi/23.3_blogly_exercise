"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag #added Tag for model update
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhh'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    """homepage shows the 5 most recent posts""" #changed from redirect to 5 most recent posts. 
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all() #pulls posts from DB, from all posts, and limits reponse to 5
    return render_template("posts/homepage.html", posts=posts)

@app.route("/users")
def users():
    """Page of all current users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """shows form for new user input"""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def new_users():
    """handles form submission of new_user_form"""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_users():
    """shows a page with info on a user using their user_id"""

    user = User.query.get_or_404(user_id) #if no user found will return the added custom 404 page. 
    return render_template('users/show.html', user=user)

@app.route("/users/<int:user_id>/edit")
def edit_users(user_id):
    """Shows the edit page for a user and a cancel button that returns to the detail page for a user, 
    and a save button that updates the user.""" 

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_users(user_id):
    """Handle the form submission for edit_users"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_users(user_id):
    """Handle the form submission for deleting a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} has been deleted.")

    return redirect("/users")

@app.errorhandler(404) #flask 404 errorhandler route
def error_page(e):
    """custom 404 error page"""
    return render_template('404.html'), 404


#posts routes for Posts model class

@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    """shows form to make a new post for user_id"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all() #add tags
    return render_template('posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_posts_form_submission(user_id):
    """Form submission for new post for user_id"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")] #convert to integer assign to tag_ids
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() #in_ is SQLAlchemy specific, filtering to make sure it exists in tag_ids.

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' has been added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """shows a page that has specific info on a post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """shows a form to edit info on a post"""    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all() #used to add tags to posts edit form
    return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_posts_form_submission(post_id):
    """post form submission handling"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'] 
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags =  Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been added.")

    return redirect(f"/users/ {post.user_id}") 

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_posts_form_submission(post_id):
    """Handles form submission to delete a post """

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been deleted.")

    return redirect(f"/users/{post.user_id}")

#add tag routes
@app.route('/tags')
def tags_index():
    """Page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def new_tags_form():
    """New tag form"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tags():
    """New tag form submission"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all() #set variable to response
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' has been added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """show info for a specific tag"""

    tag = Tag.query.get_or_404(tag_id) #prevents a non exsistent tag response
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tags_form(tag_id):
    """show form for editing a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all() 
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tags(tag_id):
    """Handle form submisson for editing a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' has been edited.")

    return render_template("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_delete(tag_id):
    """Handle form submisson for deleting a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' has been deleted.")

    return render_template("/tags")







