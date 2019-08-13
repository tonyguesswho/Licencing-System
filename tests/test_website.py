import unittest
from datetime import datetime, timedelta, timezone
from user import User
from unittest import mock
from website import Website
from utils.db import database
from app import single_plan


class WebsiteTest(unittest.TestCase):

    def setUp(self):
        self.user = User('Tony', 'Tony@test.com', 'password')

    def test_create_website(self):
        """Test creating Website object"""
        new_site = Website(self.user, 'google.com')
        self.assertEqual(new_site.user, self.user)
        self.assertEqual('google.com', new_site.url)

    def test_repr_method(self):
        """test repr method"""
        new_site = Website(self.user, 'google.com')
        self.assertEqual(f'< Website {new_site.url} belonging to {self.user}>', str(new_site))

    def test_add_site(self):
        """Test adding site to subscription"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        new_site = self.user.add_site('Andela.com')
        self.assertIsInstance(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'][0], Website)
        self.assertEqual(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'][0], new_site)
        self.assertEqual(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'][0].url, new_site.url)
        self.assertEqual(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'][0].url, 'Andela.com')
        self.assertEqual(new_site.url, 'Andela.com')

    def test_add_site_no_auth(self):
        """Test adding site to subscription without authentication fails"""
        with self.assertRaises(ValueError) as error:
            self.user.add_site('Andela.com')
        self.assertEqual('User is not authenticated', str(error.exception))

    def test_add_site_no_plan(self):
        """Test adding site without subscribing fails"""
        user = User('me', 'me@test.com', 'password')
        user.authenticated = True
        with self.assertRaises(KeyError) as error:
            user.add_site('Andela.com')
        self.assertEqual("'user has no subscription'", str(error.exception))

    def test_add_site_invalid_plan(self):
        """Test adding site to subscription above plan limit fails"""
        user = User('me2', 'me2@test.com', 'password')
        user.authenticated = True
        user.subsrcibe_to_plan(single_plan)
        user.add_site('go.com')
        with self.assertRaises(ValueError) as error:
            user.add_site('go.com')
        self.assertEqual(f"Current plan can only allow {single_plan.limit} website(s)", str(error.exception))

    def test_add_site_expired_plan(self):
        """Test adding site to  expired subscription fails"""
        user = User('me1', 'me1@test.com', 'password')
        user.authenticated = True
        user.subsrcibe_to_plan(single_plan)
        with self.assertRaises(ValueError) as error:
            with mock.patch('subscription.datetime') as mocked_date:
                mocked_date.now.return_value = datetime.now(timezone.utc)+timedelta(days=900)
                user.add_site('goal.com')
        self.assertEqual(f"Expired Subscription", str(error.exception))

    def test_update_site(self):
        """Test updating existing site"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        new_site = self.user.add_site('Andela.com')
        self.user.update_site(new_site.id, 'facebook.com')
        self.assertEqual(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'][0].url, 'facebook.com')
        self.assertEqual(new_site.url, 'facebook.com')

    def test_update_site_no_auth(self):
        """Test updating existing site without authentication fails"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        new_site = self.user.add_site('Andela.com')
        self.user.authenticated = False
        with self.assertRaises(ValueError) as error:
            self.user.update_site(new_site.id, 'facebook.com')
        self.assertEqual('User is not authenticated', str(error.exception))

    def test_update_site_no_plan(self):
        """Test updating existing site without an active subscription fails"""
        user = User('me', 'me3@test.com', 'password')
        user.authenticated = True
        with mock.patch('user.User.add_site') as mocked_add_site:
            mocked_add_site.return_value = {'id': 90}
            new_site = user.add_site('fish.com')
            with self.assertRaises(KeyError) as error:
                user.update_site(new_site['id'], 'Andela.com')
        self.assertEqual("'user has no subscription'", str(error.exception))

    def test_update_site_expired_plan(self):
        """Test updating existing site when subscription is expired fails"""
        user = User('me', 'me4@test.com', 'password')
        user.authenticated = True
        user.subsrcibe_to_plan(single_plan)
        new_site = user.add_site('Andela.com')
        with self.assertRaises(ValueError) as error:
            with mock.patch('subscription.datetime') as mocked_date:
                mocked_date.now.return_value = datetime.now(timezone.utc)+timedelta(days=900)
                user.update_site(new_site.id, 'a.com')
        self.assertEqual(f"Expired Subscription", str(error.exception))

    def test_update_invalid_site(self):
        """Test updating non existing site fails"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        with self.assertRaises(ValueError) as error:
            self.user.update_site('yu', 'facebook.com')
        self.assertEqual(f"Website does not exist", str(error.exception))

    def test_remove_site(self):
        """Test removing existing site"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        new_site = self.user.add_site('Andela.com')
        self.user.remove_site(new_site.id)
        self.assertEqual(database['subscriptions']['Tony@test.com'].websites[f'{new_site.id}'], [])

    def test_remove_site_no_auth(self):
        """Test removing existing site without authentication fails"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        new_site = self.user.add_site('Andela.com')
        self.user.authenticated = False
        with self.assertRaises(ValueError) as error:
            self.user.remove_site(new_site.id)
        self.assertEqual('User is not authenticated', str(error.exception))

    def test_remove_site_no_plan(self):
        """Test updating existing site without an active subscription fails"""
        user = User('me', 'me3@test.com', 'password')
        user.authenticated = True
        with mock.patch('user.User.add_site') as mocked_add_site:
            mocked_add_site.return_value = {'id': 90}
            new_site = user.add_site('fish.com')
            with self.assertRaises(KeyError) as error:
                user.remove_site(new_site['id'])
        self.assertEqual("'user has no subscription'", str(error.exception))

    def test_remove_site_expired_plan(self):
        """Test removing site when subscription is expired fails"""
        user = User('me', 'me4@test.com', 'password')
        user.authenticated = True
        user.subsrcibe_to_plan(single_plan)
        new_site = user.add_site('Andela.com')
        with self.assertRaises(ValueError) as error:
            with mock.patch('subscription.datetime') as mocked_date:
                mocked_date.now.return_value = datetime.now(timezone.utc)+timedelta(days=900)
                user.remove_site(new_site.id)
        self.assertEqual(f"Expired Subscription", str(error.exception))

    def test_removing_invalid_site(self):
        """Test removing non existing website fails"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        with self.assertRaises(KeyError) as error:
            self.user.remove_site('yu')
        self.assertEqual(f"'Website does not exist'", str(error.exception))


if __name__ == '__main__':
    unittest.main()
