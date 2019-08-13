import unittest
from user import User
import app
from utils.db import database


class UserTest(unittest.TestCase):

    def setUp(self):
        self.user = User('Tony', 'Tony@test.com', 'password')

    def test_create_user(self):
        """Test creating User object"""
        self.assertEqual('Tony', self.user.name)
        self.assertEqual('Tony@test.com', self.user.email)
        self.assertEqual(False, self.user.authenticated)

    def test_repr_method(self):
        """Test repr method"""
        self.assertEqual(f'< User {self.user.email}>', str(self.user))

    def test_authenticate_user_valid(self):
        """Test authenticating user with valid details"""
        self.user.authenticate('password')
        self.assertTrue(self.user.authenticated)

    def test_authenticate_user_invalid(self):
        """Test authenticating user with invalid details fails"""
        with self.assertRaises(ValueError) as error:
            self.user.authenticate('invalidpassword')
        self.assertFalse(self.user.authenticated)
        self.assertEqual('Invalid credentials', str(error.exception))

    def test_register_user(self):
        """Tes user registration"""
        new_user = app.register_user('Ify', 'ify@gmail.com', 'pass')
        self.assertIsInstance(new_user, User)
        self.assertEqual(database['users']['ify@gmail.com'], new_user)

    def test_register_user_invalid(self):
        """Test creating user with existing details fails"""
        app.register_user('me', 'me@gmail.com', 'pass')
        with self.assertRaises(ValueError) as error:
            app.register_user('me', 'me@gmail.com', 'pass')
        self.assertEqual('Email Already exists', str(error.exception))

    def test_login_user(self):
        """Test user login"""
        new_user = app.register_user('tony2', 'tony2@gmail.com', 'pass')
        app.login_user('tony2@gmail.com', 'pass')
        self.assertTrue(new_user.authenticated)

    def test_login_user_invalid_password(self):
        """Test user login with invalid password fails"""
        app.register_user('ton', 'ton@gmail.com', 'pass')
        with self.assertRaises(ValueError) as error:
            app.login_user('ton@gmail.com', 'invalidpass')
        self.assertEqual('Invalid credentials', str(error.exception))

    def test_login_user_invalid_email(self):
        """Test login user with invalid email fails"""
        app.register_user('ton1', 'ton1@gmail.com', 'pass')
        with self.assertRaises(ValueError) as error:
            app.login_user('nobody@gmail.com', 'invalidpass')
        self.assertEqual('User does not exist', str(error.exception))

    def test_save_user(self):
        """Test saving user details to database"""
        self.user.save()
        self.assertEqual(database['users']['Tony@test.com'], self.user)

    def test_save_user_invalid(self):
        """Test saving existing user details fails"""
        with self.assertRaises(ValueError) as error:
            self.user.save()
        self.assertEqual('Email Already exists', str(error.exception))


if __name__ == '__main__':
    unittest.main()
