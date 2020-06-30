class User:
    """
    #  Define a User class
    """
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def __str__(self):
        return self.username
