"""Blogly application."""
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User,Post,Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRETMAOMI"
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def show_homepage():
    """show the most recent five posts"""
    
    posts=Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html' ,posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route('/users')
def show_users():
    """
    shows list of all users in db
    Make each user a link to view the detail page for the user.
    Have a link here to the add-user form.
    """
    users=User.query.all()
    return render_template('users.html' ,users=users)

@app.route('/users/new')
def show_form():
    """Show an add form for users"""
    return render_template('new_user.html')

@app.route('/users/new' , methods=['POST'])
def create_user():
    """
    Process the add form
    adding a new user 
    and going back to /users
    """
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    new_user=User(first_name=first_name,last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """
    show details about a single user
    including a list of posts created by this user
    """
    user=User.query.get_or_404(user_id)
    posts=Post.query.filter(Post.creater==user_id).all()
    return render_template('details.html', user=user,posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """
    Show the edit page for a user.
    Have a cancel button that returns to the detail page for a user, 
    and a save button that updates the user.
    """
    user=User.query.get_or_404(user_id)
    return render_template("edit.html",user=user)

@app.route("/users/<int:user_id>/edit" ,methods=['POST'])
def process_edit(user_id):
    """
    Process the edit form, returning the user to the /users page.
    """
    user=User.query.get_or_404(user_id)
    user.first_name=request.form["first_name"]
    user.last_name=request.form["last_name"]
    user.image_url=request.form["image_url"]
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """
    Delete the user.
    """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")


# Add Post Routes

@app.route("/users/<int:user_id>/posts/new")
def show_newpost_form(user_id):
    """
    GET /users/[user_id]/posts/new
    Show form to add a post for that user.
    """
    user=User.query.get_or_404(user_id)
    tags=Tag.query.all()
    return render_template("post_form.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_new_post(user_id):
    """
    POST /users/[user_id]/posts/new
    Handle add form; add new post to db
    add post and redirect to the user detail page.

    #Update# the route for adding posts
    so that it shows a listing of the tags 
    and lets you pick which tag(s) apply to that post.
    """
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    u=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """
    Show a post
    Show buttons to edit and delete the post.
    #Update# this route so that it shows all the tags for the post.
    """
    post=Post.query.get_or_404(post_id)
    tags=post.tags
    return render_template("post_detail.html", post=post, tags=tags)
    

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """
    GET /posts/[post_id]/edit
    Show form to edit a post, and to cancel (back to user page).
    """
    post=Post.query.get_or_404(post_id)
    tags=Tag.query.all()
    return render_template("post_edit.html",post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_post_edit(post_id):
    """
    POST /posts/[post_id]/edit
    Handle editing of a post. Redirect back to the post view.
    """
    post=Post.query.get_or_404(post_id)
    post.title=request.form["title"]
    post.content=request.form["content"]
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """
    POST /posts/[post_id]/delete
    Delete the post.
    """
    post=Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post.creater}")


@app.route("/tags")
def list_tags():
    """
    GET /tags. Lists all tags, with links to the tag detail page.
    """
    tags=Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):
    """
    GET /tags/[tag-id]
    Show detail about a tag. 
    Show posts that have this tag
    Have links to edit form and to delete.
    """
    tag=Tag.query.get_or_404(tag_id)
    posts=tag.posts
    return render_template("tag_detail.html", tag=tag, posts=posts )

@app.route("/tags/new")
def show_tag_form():
    """
    GET /tags/new
    Shows a form to add a new tag.
    """
    return render_template("new_tag_form.html")

@app.route("/tags/new", methods=["POST"])
def process_add_form():
    """
    POST /tags/new
    Process add form, adds tag, and redirect to tag list.
    """
    name=request.form["name"]
    new_tag=Post(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_tag_edit_form(tag_id):
    """
    GET /tags/[tag-id]/edit
    Show edit form for a tag.
    """
    tag=Tag.query.get_or_404(tag_id)
    return render_template("tag_edit_form.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit" , methods=["POST"])
def process_tag_edit_form(tag_id):
    """
    POST /tags/[tag-id]/edit
    Process edit form, edit tag, and redirects to the tags list.
    """
    tag=Tag.query.get_or_404(tag_id)
    tag.name=request.form["name"]
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """
    POST /tags/[tag-id]/delete
    Delete a tag.
    """
    Post.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect("/tags")

    












