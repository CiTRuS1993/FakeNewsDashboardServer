
from BuisnessLayer.Users.UsersManagerFacade import UserManagerFacade


class UsersManagerInterface:

    def __init__(self, username, password):
        self.userManagerLogic=UserManagerFacade(username, password)

    def saveSearchTweetsByKeywords(self, username, search_id):
        pass

    def login(self, username, password):
        pass

    def register(self, username, password):
        pass

    def classifyTweets(self, username, classify_id):
        pass

    def tagTweet(self, username, tweet_id):
        pass

    def validateUser(self, username, password):
        pass

    def deleteUser(self, admin_username, username_to_delete):
        if self.userManagerLogic.is_admin(admin_username):
            self.userManagerLogic.delete_user(username_to_delete)

    def viewUserSearchHistory(self, username, username_to_view):
        if self.userManagerLogic.is_admin(username) or username == username_to_view:
            return self.userManagerLogic.view_user_search_history(username_to_view)
        return False # TODO- exception?

    def is_admin(self, username):
        return self.userManagerLogic.is_admin(username)

    def userExists(self, username):
        return self.userManagerLogic.user_exists(username)

