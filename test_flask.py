from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogy_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BlogUsersTestCase(TestCase):
    """Tests for Blogy."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestFisrtName", last_name="TestLastName", image_url="https://c.ndtvimg.com/2020-08/h5mk7js_cat-generic_625x300_28_August_20.jpg?im=Resize=(1230,900)")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFisrtName', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>User Detail Page</h1>", html)


    def test_show_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Create a user</h2>', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstName2", "last_name": "TestLastName2", "image_url": "https://images2.minutemediacdn.com/image/upload/c_crop,h_1600,w_2378,x_11,y_0/v1628778532/shape/mentalfloss/87226-gettyimages-1247734973.jpg?itok=wNVO1JQG"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirstName2", html)
    

    def test_delete_user(self):
        with app.test_client() as client:
            resp=client.post(f"/users/{self.user_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("TestFirstName", html)



