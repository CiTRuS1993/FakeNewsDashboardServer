from BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager import GoogleTrendsManager
from BuisnessLayer.ExternalSystemsAPIsManager.TwitterManagerStub import TwitterManagerStub


class ExternalSystemsFacade:
    def __init__(self):
        self.googleTrendsManager = GoogleTrendsManager()
        self.twitterManager = TwitterManagerStub()
        self.googleTrendsManager.connect()
        self.twitterManager.connect()
        self.twitterManager.search_tweets_by_trends(self.googleTrendsManager.get_trends())

    def search_tweets_by_keywords(self, keyword: str, token=None):
        return self.twitterManager.search_tweets_by_keywords(keyword, token)

    def retrieve_google_trends_data(self):
        self.twitterManager.stop()
        tweets = self.twitterManager.get_unprocessed_tweets()
        self.twitterManager.search_tweets_by_trends(self.googleTrendsManager.get_trends())
        return tweets

    def edit_twitters_tokens(self, tokens):
        return self.twitterManager.edit_tokens(tokens)
