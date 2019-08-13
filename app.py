from utils.db import database
from user import User
from plan import Plan


single_plan = Plan('Single', 49, 1)
plus_plan = Plan('Plus', 99, 3)
infinite_plan = Plan('Infinite', 249, None)


def register_user(name, email, password):
    if email in database['users']:
        raise ValueError('Email Already exists')
    new_user = User(name, email, password)
    new_user.save()
    return new_user


def login_user(email, password):
    if email not in database['users']:
        raise ValueError('User does not exist')
    user = database['users'].get(f'{email}')
    user.authenticate(password)
    return user


# new_user = User('tony', 'tony@gmail.com', 'password')
# new_user.add_site('google.com')
# user = register_user('tony', 'tonyp@gmail.com', 'password')
# user = login_user('tonyp@gmail.com', 'password')
# user.subsrcibe_to_plan(single_plan)
# user.change_plan(plus_plan)
# new_site = user.add_site('google.com')
# user.add_site('googlel.com')
# user.update_site(new_site.id, 'bing.com')
# user.remove_site(new_site.id)
