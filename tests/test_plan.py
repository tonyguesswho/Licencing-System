import unittest
from plan import Plan
from user import User
from subscription import Subscription
from app import single_plan, plus_plan
from utils.db import database


class PlanTest(unittest.TestCase):

    def setUp(self):
        self.user = User('Tony', 'Tony@test.com', 'password')
        self.plan = single_plan

    def test_create_plan(self):
        """Test creating a Plan object"""
        plan = Plan('Test', 50, 5)
        self.assertEqual('Test', plan.name)
        self.assertEqual(50, plan.price)
        self.assertEqual(5, plan.limit)

    def test_repr_method(self):
        """test repr method"""
        plan = Plan('Test', '50', 5)
        self.assertEqual(f'< Plan {plan.limit}>', str(plan))

    def test_get_plan(self):
        """test getting plan associated with a subscription"""
        new_sub = Subscription(self.user, self.plan)
        result = new_sub.get_plan()
        self.assertEqual(result, new_sub.plan)

    def test_update_plan(self):
        """Test updating existing plan in a subscription"""
        self.user.authenticated = True
        self.user.subsrcibe_to_plan(single_plan)
        self.user.change_plan(plus_plan)
        self.assertIsInstance(database['subscriptions']['Tony@test.com'].plan, Plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan, plus_plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan.limit, plus_plan.limit)

    def test_change_plan_no_auth(self):
        """Test updating plan without authentication fails"""
        with self.assertRaises(ValueError) as error:
            self.user.change_plan(plus_plan)
        self.assertEqual('User is not authenticated', str(error.exception))

    def test_change_plan_no_initial_plan(self):
        """Test using the change_plan method to create a new subscription/plan"""
        self.user.authenticated = True
        self.user.change_plan(single_plan)
        self.assertIsInstance(database['subscriptions']['Tony@test.com'].plan, Plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan, single_plan)
        self.assertEqual(database['subscriptions']['Tony@test.com'].plan.limit, single_plan.limit)


if __name__ == '__main__':
    unittest.main()
