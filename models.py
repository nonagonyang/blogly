"""Models for Blogly."""
# Create User Model
from typing_extensions import Self
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create SQLAlchemy instance and save into the variable db
db=SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below
"""create a User model for SQLAlchemy. 
It should have the following columns:
id, an autoincrementing integer number that is the primary key
first_name and last_name
image_url for profile images
"""


class User(db.Model):
    __tablename__='users'
    def __repr__(self):
        u=self
        return f"<User id={u.id} firstname={u.first_name} lastname={u.last_name} image_url={u.image_url}>"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    first_name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=True)
    image_url=db.Column(db.String(200),nullable=True)



# Post should have an:
# id, like for User
# title
# content
# created_at a date+time that should automatically default to the when the post is created
# a foreign key to the User table

class Post(db.Model):
    __tablename__="posts"
    def __repr__(self):
        p=self 
        return f"<Post id={p.id} title={p.title}> content={p.content} created_at={p.created_at}"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.String,nullable=False)
    created_at=db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    creater = db.Column(db.Integer,db.ForeignKey('users.id'))

    u = db.relationship('User',backref='posts')
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")