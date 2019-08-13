from datetime import datetime, timezone, timedelta
from utils.db import database
from collections import defaultdict


class Subscription():
    """
    This is a class for the subscription and subscription operations.

    """
    def __init__(self, user, plan):
        """
        The constructor for the Subscription class.

        Parameters:
           user (obj): The user object.
           plan (obj): The user's plan object.
        """
        self.user = user
        self.start_date = datetime.now(timezone.utc)
        self.plan = plan
        self.websites = defaultdict(list)

    def __repr__(self):
        return f'<Subcription with {self.plan} plan>'

    @property
    def get_end_date(self):
        """
        The function to get end date of user's plan.

        Parameters:
            plan (Object): plan object.

        Returns:
            datetime: Expiry date of user's plan.
        """
        return self.start_date + timedelta(days=365)

    def get_plan(self):
        """
        The function to get user's plan.

        Parameters:
            plan (Object): plan object.

        Returns:
            datetime: Users plan.
        """
        return self.plan

    def save(self):
        """
        The function to save subscription to database.

        Parameters:
          subscription   (obj): subscription object to be saved.
        """
        database['subscriptions'][f'{self.user.email}'] = self

    def check_sub(subscription):
        """
        The function to check validity of a subscription.

        Parameters:
          subscription   (obj): subscription object.
        """
        if (subscription.get_end_date < datetime.now(timezone.utc)):
            raise ValueError('Expired Subscription')
