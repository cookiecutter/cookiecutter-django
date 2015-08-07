from test_plus.test import TestCase


class TestUser(TestCase):

    def test__str__(self):
        user = self.make_user()
        self.assertEqual(
            user.username,
            "testuser"  # This is the default username for self.make_user()
        )
