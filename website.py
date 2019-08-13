import uuid


class Website:
    """
    This is a class for the website.

    """
    def __init__(self, user, url):
        """
        The constructor for the Website class.

        Parameters:
           user (obj): The user object.
           url (str): The websites url.
        """
        self.user = user
        self.url = url
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'< Website {self.url} belonging to {self.user}>'
