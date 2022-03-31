from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)


        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        user_post = Post(title="test_title_2", content = "test_content_2",user_id = self.user_id)
        db.session.add_all([user_post])
        db.session.commit()

        self.user_post = user_post

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_new_post(self):
        """Check new posts created are saved to database"""
        with self.client as c:
            resp=c.post(f"/users/{self.user_id}/posts/new",
                data =
                        {'title':'test_title',
                        'content':'test_content',
                        'user_id': self.user_id},
                follow_redirects = True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_title",html)

    def test_edit_post(self):
        """Check edits to post are updated on database"""
        with self.client as c:
            resp=c.post(f"/posts/{self.user_post.id}/edit",
                data =
                        {'title':'test_title_2_edited',
                        'content':'test_content_2_edited',
                        'user_id': self.user_id},
                follow_redirects = True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_title_2_edited",html)

    def test_delete_post(self):
        """Check there is one less post in database after delete action."""
        posts_before = len(Post.query.all())

        with self.client as c:
            # breakpoint()
            resp= c.post(f"/posts/{self.user_post.id}/delete",
                        follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            posts_after = len(Post.query.all())
            self.assertEqual(posts_after + 1 , posts_before)

            html = resp.get_data(as_text=True)
            self.assertNotIn('test_title_2',html)

