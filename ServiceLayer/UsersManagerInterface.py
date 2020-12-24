
from BuisnessLayer.Users.UsersManagerFacade import UserManagerFacade


class UsersManagerInterface:

    def __init__(self, username, password):
        self.userManagerLogic=UserManagerFacade(username, password)

    def saveSearchTweetsByKeywords(self, username, search_id):
        return self.userManagerLogic.save_search_tweets_by_keywords(username, search_id)

    def login(self, username, password):
        return self.userManagerLogic.login(username, password)

    def register(self, username, password):
        return self.userManagerLogic.register(username, password)

    def classifyTweets(self, username, classify_id):
        return self.userManagerLogic.classify_tweets(username, classify_id)

    def tagTweet(self, username, tweet_id):
        return self.userManagerLogic.tag_tweet(username, tweet_id)

    def validateUser(self, username, password):
        return self.userManagerLogic.validate_user(username, password)

    def deleteUser(self, admin_username, username_to_delete):
        if self.userManagerLogic.is_admin(admin_username):
            return self.userManagerLogic.delete_user(username_to_delete)
        return False # TODO- exception?

    def viewUserSearchHistory(self, username, username_to_view):
        if self.userManagerLogic.is_admin(username) or username == username_to_view:
            return self.userManagerLogic.view_user_search_history(username_to_view)
        return False # TODO- exception?

    def is_admin(self, username):
        return self.userManagerLogic.is_admin(username)

    def userExists(self, username):
        return self.userManagerLogic.user_exists(username)

