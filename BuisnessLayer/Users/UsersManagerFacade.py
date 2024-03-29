import sys
from BuisnessLayer.Users.User import User
from PersistenceLayer.UsersORM.UsersORMFacade import UsersORMFacade


class UserManagerFacade:

    def __init__(self, username, password):
        self.users_db = UsersORMFacade()
        self.users_by_name_list = self.initUsersDB()

        if not self.admin_exists(username, password):
            sys.exit("Wrong username or password!")

    def initUsersDB(self):
        users = self.users_db.get_all_users()
        users_dict = {}
        for user in users:
            users_dict[user['username']] = User(user['role'], user['email'], user['username'], user['password'])
        return users_dict

    def admin_exists(self, username, password):
        if username in self.users_by_name_list.keys():
            if self.users_by_name_list[username].password == password:
                return True
        return False

    def save_search_tweets_by_keywords(self, username, search_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].save_search_tweets_by_keywords(search_id)
            return True
        return False


    def tag_tweet(self, username, tweet_id):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].tag_tweet(tweet_id)
            return True


    def get_role(self, username):
        if username in self.users_by_name_list.keys():
            self.users_by_name_list[username].get_role()
            return True

    def view_user_search_history(self, username):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].view_user_search_history()
        return False

    def register(self, username, password):
        if username not in self.users_by_name_list.keys():
            self.users_by_name_list[username] = User("Registered", len(self.users_by_name_list) + 1, username, password,
                                                     {}, [], -1)
            return True
        return False

    def login(self, username, password):
        return self.validate_user(username, password)

    def delete_user(self, username):
        if username in self.users_by_name_list.keys():
            del self.users_by_name_list[username]
            return True
        return False

    def is_admin(self, username):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].role == "admin"
        return False

    def validate_user(self, username, password):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].check_password(password)
        return False

    def classify_tweets(self, username, classify_id):
        if username in self.users_by_name_list.keys():
            return self.users_by_name_list[username].classify_tweets(classify_id)
        return False

    def user_exists(self, username):
        return username in self.users_by_name_list.keys()







