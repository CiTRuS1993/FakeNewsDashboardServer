import sys
from BuisnessLayer.Users.User import User


class UserManagerFacade:

    def __init__(self, username, password):
        self.users_by_name_list = self.initUsersDB()
        if not self.adminExists(username, password):
            sys.exit("Wrong username or password!")

    def init_users_db(self):
        return {"username": "username", "password": "pass"}

    def admin_exists(self, username, password):
        if username in self.users_by_name_list.keys():
            pass
        return True

    def save_search_tweets_by_keywords(self, username, search_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].save_search_tweets_by_keywords(search_id)

    def tag_tweet(self, username, tweet_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].tag_tweet(tweet_id)

    def get_role(self, username):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].get_role()

    def view_user_search_history(self, username):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].view_user_search_history()

    def register(self, username, password):
        if username not in self.users_by_name_list.keys():
            self.users_by_name_list[username] = User(self, "Registered", self.users_by_name_list(dict)+1, password, {}, [])

    def login(self, username, password):
        return self.validate_user(username, password)

    def delete_user(self, username):
        if username in self.users_by_name_list.keys():
            del self.users_by_name_list[username]

    def is_admin(self, username):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].get_role == "admin"

    def validate_user(self, username, password):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].check_password(password)
        return False

    def classify_tweets(self, username, classify_id):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].classify_tweets(classify_id)
        pass

    def user_exists(self, username):
        return username in self.users_by_name_list.keys()







