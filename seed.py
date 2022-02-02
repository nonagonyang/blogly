"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
LouiseGlück = User(first_name='Louise',last_name='Glück',image_url="https://i.guim.co.uk/img/media/84fe7eaee6f9e2ffcb525bd81eade9c0e8a2253a/0_151_2836_1702/master/2836.jpg?width=700&quality=85&auto=format&fit=max&s=92a56dd981be97001c028132d57d02d5")
PeterHandke= User(first_name='Peter',last_name='Handke',image_url="https://upload.wikimedia.org/wikipedia/commons/e/ea/Peter-handke.jpg")
OlgaTokarczuk= User(first_name='Olga',last_name='Tokarczuk',image_url="https://cdn.britannica.com/92/212492-050-F688647D/Olga-Tokarczuk-Polish-writer-Nobel-Prize-literature-2019.jpg")

# Add new objects to session, so they'll persist
db.session.add(LouiseGlück)
db.session.add(PeterHandke)
db.session.add(OlgaTokarczuk)

# Commit--otherwise, this never gets saved.
db.session.commit()