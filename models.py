"""Models for Blogly."""
# Create User Model
from flask_sqlalchemy import SQLAlchemy

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

    def greet(self):
        return f"Hi, I am {self.name} the {self.spieces}"