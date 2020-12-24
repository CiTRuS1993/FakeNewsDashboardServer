import sys

class UserManagerFacade:

    def __init__(self, username, password):
        self.initUsersDB()
        if not self.adminExists(username, password):
            sys.exit("Wrong username or password!")

    def initUsersDB(self):
        pass

    def adminExists(self, username, password):
        pass