import sys
class UserManagerFacade:

    def __init__(self, username, password):
        self.users_by_name_list = self.initUsersDB()
        if not self.adminExists(username, password):
            sys.exit("Wrong username or password!")

    def init_users_db(self):
        return {"username": "username","password": "pass"}

    def admin_exists(self, username, password):
        if username in self.users_by_name_list.keys():
            pass
        return True

    def save_search_tweets_by_keywords(self, username ,search_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username]

    def tag_tweet(self, username, tweet_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].tag_tweet(tweet_id)

    def get_role(self,username):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].get_role()

    def view_user_search_history(self, username):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].view_user_search_history