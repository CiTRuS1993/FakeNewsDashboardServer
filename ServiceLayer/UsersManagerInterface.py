
from BuisnessLayer.Users.UsersManagerFacade import UserManagerFacade


class UsersManagerInterface:

    def __init__(self, username, password):
        self.userManagerLogic=UserManagerFacade(username, password)

