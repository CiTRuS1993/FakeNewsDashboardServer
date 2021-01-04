import threading
import time


class TwitterManagerStub:
    def __init__(self):
        self.unprocessed_tweets = {}
        self.tokens = ["my token"]
        self.twitter_api = "something"
        self.search = False

    def connect(self):
        pass

    def search_tweets_by_keywords(self, keywords, token=None, on_finished=lambda tweets: print(tweets)):
        tweets = {}
        for keyword in keywords:
            if keyword in tweets.keys():
                tweets[keyword].append("hey I'm a tweet!")
            else:
                tweets[keyword] = ["hey I'm also a tweet!"]
            time.sleep(1)
        on_finished(tweets)
        return tweets

    def stop(self):
        self.search = False

    def search_tweets_by_trends(self, trends):
        def search_trends():
            while self.search:
                for trend in trends:
                    new_tweets = self.search_tweets_by_keywords(trend, self.tokens[0])
                    for key in new_tweets.keys():
                        self.unprocessed_tweets[key] = new_tweets[key]
                    if not self.search:
                        return

        search_thread = threading.Thread(target=search_trends)
        self.search = True
        search_thread.start()

    def edit_tokens(self, tokens):
        for token in tokens:
            self.tokens.append(token)

    def get_unprocessed_tweets(self):
        tweets = self.unprocessed_tweets
        self.unprocessed_tweets = {}
        return tweets
