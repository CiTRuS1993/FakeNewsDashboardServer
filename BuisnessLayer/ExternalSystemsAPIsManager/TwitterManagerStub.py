class TwitterManagerStub:
    def __init__(self):
        self.unprocessed_tweets = {}
        self.tokens = ["my token"]
        self.twitter_api = "something"

    def connect(self):
        pass

    def search_tweets_by_keywords(self, keywords, token=None, on_finished=lambda tweets: print("find")):
        tweets = {}
        for keyword in keywords.split(','):
            if keyword in self.unprocessed_tweets.keys():
                tweets[keyword].append("hey I'm a tweet!")
            else:
                tweets[keyword] = ["hey I'm also a tweet!"]
        on_finished(tweets)
        return tweets

    def search_tweets_by_trends(self, trends):
        for trend in trends:
            new_tweets = self.search_tweets_by_keywords(trend, self.tokens.pop())
            for key in new_tweets.keys():
                self.unprocessed_tweets[key] = new_tweets[key]

    def edit_tokens(self, tokens):
        for token in tokens:
            self.tokens.append(token)
