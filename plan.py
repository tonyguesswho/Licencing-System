
class Plan():
    """
    This is a class for the plans.

    """
    def __init__(self, name, price, limit):
        """
        The constructor for the Subscription class.

        Parameters:
           name (str): The plan name.
           price (int): The plan price.
           limit (int): Allowed nuber of websites.
        """
        self.name = name
        self.price = price
        self.limit = limit

    def __repr__(self):
        return f'< Plan {self.limit}>'
