class User:

    def __init__(self, role, user_id, username, password, search_history=[], tagged_tweets=[],classify_id=-1):
        self.role = role
        self.user_id = user_id
        self.username = username
        self.password = password
        self.search_history = search_history
        self.classify_id = classify_id
        self.tagged_tweets = tagged_tweets
        self.logged_in = False

    def save_search_tweets_by_keywords(self, search_id):
        self.search_history.append(search_id)
        return True

    def tag_tweet(self, tweet_id):
        if tweet_id not in self.tagged_tweets:
            self.tagged_tweets.append(tweet_id)
            return True
        return False

    def get_role(self):
        return self.role

    def check_password(self, password):
        return self.password == password

    def view_user_search_history(self):
        return self.search_history

    def classify_tweets(self, classify_id):
        self.classify_id = classify_id
        return True

    def logged_id(self):
        return self.logged_in

    def login(self, password):
        if self.password == password:
            self.logged_in = False
            return True
        return False

    def logout(self):
        self.logged_in = False










