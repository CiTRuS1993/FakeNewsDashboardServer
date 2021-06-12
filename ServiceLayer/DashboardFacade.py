import time

from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface
from ServiceLayer.UsersManagerInterface import UsersManagerInterface
import threading

class DashboardFacade:

    def __init__(self, username, password):
        self.analysisManager=AnalysisManagerInterface()
        self.externalSystemsManager=ExternalSystemsAPIsManagerInterface()
        self.usersManager=UsersManagerInterface(username, password)
        self.trends_timer = threading.Timer(12.0*360, self.retrieveGoogleTrendsData)
        # self.snopes_timer = threading.Timer(12.0*360, self.retrieveSnopesData)
        time.sleep(20)
        # retrieve data from Google Trends and from Snopes
        # self.retrieveGoogleTrendsData()
        # self.retrieveSnopesData()     TODO- uncomment
        # TODO- add func which sends each unclassified tweet to analysisManager (errors handling)
# ------------------------------- Retrieve Data & External Systems -----------------------------

    # gets all data related to the dashboard
    # def retrieveFakeNewsData(self):
    #     return self.analysisManager.retrieveFakeNewsData()

    # gets all data related to the Google Trends window
    def googleTrendsStatistics(self):
        # self.retrieveGoogleTrendsData()
        ans = self.analysisManager.getGoogleTrendsStatistics()
        # print(f"get = {ans}")
        return ans
        # return self.analysisManager.getGoogleTrendsStatistics()

    # gets all data related to the Snopes window
    def snopesStatistics(self):
        return self.analysisManager.getSnopesStatistics()

    # each 12 hours retrieve the new Google Trends topics
    def retrieveGoogleTrendsData(self):
        new_trends= self.externalSystemsManager.retrieveGoogleTrendsData()
        # print(f"new trends are: {new_trends}")
        return self.analysisManager.classifyTrends(new_trends)

    # each 12 hours retrieve the new Snopes claims
    def retrieveSnopesData(self):
        new_claims= self.externalSystemsManager.retrieveSnopesData()
        return self.analysisManager.classifySnopes(new_claims)

    def configClassifier(self, username, classifier, configuration):
        if self.usersManager.is_admin(username):
            return self.analysisManager.configClassifier(classifier, configuration)
        return False # maybe exception?

    def getTemperature(self):
        return self.analysisManager.getTemperature()

    def get_emotions(self):
        return self.analysisManager.get_emotions()

    def get_sentiment(self):
        return self.analysisManager.get_sentiment()

    def get_topic(self, topic_id):
        return self.analysisManager.get_topic(topic_id)

    def get_topics(self, trend_id):
        return self.analysisManager.get_topics(trend_id)

    def get_emotion_tweets(self, emotion):
        return self.analysisManager.get_emotion_tweets(emotion)

# ----------------------------------- Users Options ------------------------------------------

    def searchTweetsByKeywords(self, username, keyword, token=None):
        if (self.usersManager.userExists(username)):
            search_id= self.externalSystemsManager.searchTweetsByKeywords(keyword, token)
            self.usersManager.saveSearchTweetsByKeywords(username, search_id)
            return True
        return False

    def tagTweet(self, username, tweet_id, isFake):
        if self.usersManager.userExists(username):
            self.analysisManager.tagTweets(tweet_id, isFake)
            self.usersManager.tagTweet(username, tweet_id)

    def viewUserSearchHistory (self, username, username_to_view):
        return self.usersManager.viewUserSearchHistory(username,username_to_view)

    def editTwittersTokens(self, username, tokens):
        if self.usersManager.is_admin(username):
            return self.externalSystemsManager.editTwittersTokens(tokens)
        return False

    def classifyTweets(self, username, file):
        if (self.usersManager.userExists(username)):
            classify_id=self.analysisManager.classifyTweets(file)
            return self.usersManager.classifyTweets(username, classify_id)
        return False # maybe exception?

# ----------------------------------- Manage Users --------------------------------------------

    def register(self, username, password):
        return self.usersManager.register(username,password)

    def login(self, username, password):
        return self.usersManager.login(username,password)

    def deleteUser(self, admin_username, username_to_delete):
        return self.usersManager.deleteUser(admin_username, username_to_delete)






