from utils.db import database
from subscription import Subscription
from website import Website
from utils.helpers import check_key


class User:
    """
    This is a class for the user and all user's operations.

    """
    def __init__(self, name, email, password):
        """
        The constructor for the User class.

        Parameters:
           name (str): The user's name.
           email (str): The user's email.
           password (str): The user's password.
        """
        self.name = name
        self.email = email
        self.__password = password
        self.authenticated = False

    def __repr__(self):
        return f'< User {self.email}>'

    def authenticate(self, password):
        """
        The function to authenticate the user.

        Parameters:
            password (str): The user's password.
        """
        if(password == self.__password):
            self.authenticated = True
        else:
            raise ValueError('Invalid credentials')

    def subsrcibe_to_plan(self, plan):
        """
        The function to enable user's subscribe to a plan.

        Parameters:
            plan (Object): The Plan to be subscribed to.

        Returns:
            Object: A subscription object contain details of the subscription.
        """
        self.check_auth()
        new_sub = Subscription(self, plan)
        new_sub.save()
        return new_sub

    def check_auth(self):
        """
        The function to check if user is authenticated.

        Parameters:
            user (Object): User's object

        """
        if not self.authenticated:
            raise ValueError('User is not authenticated')

    def change_plan(self, plan):
        """
        The function to enable user change plan.

        Parameters:
            plan (Object): New Plan to be subscribed to.

        """
        self.check_auth()
        subscription = database['subscriptions'].get(f'{self.email}')
        if not subscription:
            return self.subsrcibe_to_plan(plan)
        subscription.plan = plan

    def add_site(self, url):
        """
        The function to enable user's add website.

        Parameters:
            url (str): Url of the website.

        Returns:
            Object: Website object with details of the website.
        """
        self.check_auth()
        subscription = database['subscriptions'].get(f'{self.email}')
        check_key(subscription, 'user has no subscription')
        subscription.check_sub()
        site_limit = subscription.plan.limit
        if site_limit and (site_limit == len(subscription.websites)):
            raise ValueError(f'Current plan can only allow {site_limit} website(s)')
        new_site = Website(self, url)
        subscription.websites[f'{new_site.id}'].append(new_site)
        subscription.save()
        return new_site

    def update_site(self, site_id, new_url):
        """
        The function to enable user's update website.

        Parameters:
            new_url (str): Url of the new website.
            site_id (str): id of the new website to be updated.

        Returns:
            Object: Website object with details of the update website.
        """
        self.check_auth()
        subscription = database['subscriptions'].get(f'{self.email}')
        check_key(subscription, 'user has no subscription')
        subscription.check_sub()
        if not subscription.websites[f'{site_id}']:
            raise ValueError('Website does not exist')
        subscription.websites[f'{site_id}'][0].url = new_url
        subscription.save()
        updated_site = subscription.websites[f'{site_id}'][0]
        return updated_site

    def remove_site(self, site_id):
        """
        The function to enable user's remove website from a plan.

        Parameters:
            site_id (str): id of the new website to be removed.
        """
        self.check_auth()
        subscription = database['subscriptions'].get(f'{self.email}')
        check_key(subscription, 'user has no subscription')
        subscription.check_sub()
        check_key(subscription.websites[f'{site_id}'], 'Website does not exist')
        del subscription.websites[f'{site_id}']

    def save(self):
        """
        The function to save user to database.

        Parameters:
            user (obj): user object to be saved.
        """
        if self.email in database['users']:
            raise ValueError('Email Already exists')
        database['users'][f'{self.email}'] = self
