"""Blogly application."""
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
def list_users():
    """Redirect to list of users. (We will fix this in a later step)."""
    users=User.query.all()
    return render_template('users.html' ,users=users)


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
    """show details about a single user"""
    user=User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

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
