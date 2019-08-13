import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock
from subscription import Subscription
from app import single_plan
from user import User
from utils.db import database
from plan import Plan


class SubscriptionTest(unittest.TestCase):

    def setUp(self):
        self.user = User('Tony', 'Tony@test.com', 'password')
        self.plan = single_plan

    def test_create_subscription(self):
        """Test creating subscription object"""
        with mock.patch('subscription.datetime') as mocked_date:
            mocked_date.now.return_value = datetime(2019, 1, 1)
            new_sub = Subscription(self.user, self.plan)
            self.assertEqual(new_sub.user, self.user)
            self.assertEqual(new_sub.plan, self.plan)
            self.assertDictEqual(new_sub.websites, {})
            self.assertEqual(new_sub.start_date, datetime(2019, 1, 1))
            self.assertEqual(new_sub.get_end_date, datetime(2019, 1, 1) + timedelta(days=365))

    def test_repr_method(self):
        """Test repr method"""
        new_sub = Subscription(self.user, self.plan)
        self.assertEqual(f'<Subcription with {self.plan} plan>', str(new_sub))

    def test_valid_sub(self):
        """Test user subscription is still valid"""
        new_sub = Subscription(self.user, self.plan)
        new_sub.check_sub()
        self.assertTrue(new_sub.get_end_date > datetime.now(timezone.utc))

    def test_save_sub(self):
        """Test saving subscription to the database"""
        new_sub = Subscription(self.user, self.plan)
        new_sub.save()
        self.assertEqual(database['subscriptions']['Tony@test.com'], new_sub)

    def test_subscribe_plan(self):
        """Test user subscribing to a plan"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        self.assertIsInstance(database['subscriptions']['Tony@test.com'].plan, Plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan, single_plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan.limit, 1)

    def test_subscribe_plan_no_auth(self):
        """Test user subscribing to a plan without authentication fails"""
        with self.assertRaises(ValueError) as error:
            self.user.subsrcibe_to_plan(single_plan)
        self.assertEqual('User is not authenticated', str(error.exception))


if __name__ == '__main__':
    unittest.main()
