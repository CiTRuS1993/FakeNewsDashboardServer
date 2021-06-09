from BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager import GoogleTrendsManager
from BuisnessLayer.ExternalSystemsAPIsManager.snopesManager import SnopesManager
from BuisnessLayer.ExternalSystemsAPIsManager.TwitterManager import TwitterManager


class ExternalSystemsFacade:
    def __init__(self):
        self.googleTrendsManager = GoogleTrendsManager()
        self.twitterManager = TwitterManager()
        self.snopesManager = SnopesManager()
        # self.snopesManager.start()
        self.googleTrendsManager.connect()
        self.twitterManager.connect()
        self.twitterManager.search_tweets_by_trends(self.googleTrendsManager.get_trends())

    def search_tweets_by_keywords(self,search_id, keyword: str, token=None):
        return self.twitterManager.search_tweets_by_keywords(search_id, keyword, token)

    def retrieve_google_trends_data(self):
        self.twitterManager.stop()
        tweets = self.twitterManager.get_unprocessed_tweets()
        self.googleTrendsManager.connect()
        self.twitterManager.search_tweets_by_trends(self.googleTrendsManager.get_trends())
        return tweets

    def edit_twitters_tokens(self, tokens):
        return self.twitterManager.edit_tokens(tokens)

    def retrieve_snopes_data(self):
        # TODO - retrieve tweets
        return self.snopesManager.get_snopes() # maybe another func?
