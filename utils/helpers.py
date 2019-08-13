def check_key(item, message):
    """
    Check  Valid key.

    Function checks if a value is a dictionary key.

    Parameters:
    item (int): Value from trying to get a key from dictionary
    mesaage (int): describs error messahe if value is not a valid key

    """
    if not item:
        raise KeyError(message)
