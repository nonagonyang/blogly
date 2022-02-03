"""Seed file to make sample data for users db."""

from models import User,Post, db
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
MatsuoBasho=User(first_name="Matsuo", last_name="Basho",image_url="https://api.poets.org/sites/default/files/styles/poem_a_day_portrait/public/images/biographies/Basho_by_Buson.png?itok=qCZYXLvu")




# Add new objects to session, so they'll persist
db.session.add_all([LouiseGlück,PeterHandke,OlgaTokarczuk,MatsuoBasho])

# Commit--otherwise, this never gets saved.
db.session.commit()


# Add posts
post1=Post(title="Do not go gentle into that good night", content="""Do not go gentle into that good night,
Old age should burn and rave at close of day;
Rage, rage against the dying of the light.""", creater=1)
post2=Post(title="This Is Not a Small Voice", content="""This is not a small voice
you hear this is a large voice coming out of these cities.""", creater=1)
post3=Post(title="The cry of the cicada", content="""The cry of the cicada
Gives us no sign That presently it will die.""", creater=1)
post4=Post(title="I come weary," , content="""I come weary,In search of an inn—Ah! These wisteria flowers!""",creater=4)
post5=Post(title="An ancient pond!", content="""An ancient pond! With a sound from the water Of the frog as it plunges in.""",creater=4)

db.session.add_all([post1, post2, post3,post4,post5])
db.session.commit()