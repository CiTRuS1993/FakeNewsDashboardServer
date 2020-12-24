from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface
from ServiceLayer.UsersManagerInterface import UsersManagerInterface


class DashboardFacade:

    def __init__(self, username, password):
        self.analysisManager=AnalysisManagerInterface()
        self.externalSystemsManager=ExternalSystemsAPIsManagerInterface()
        self.usersManager=UsersManagerInterface(username, password)


    def retrieveGoogleTrendsData(self):
        pass

    def searchTweetsByKeywords(self, username, keywords):
        pass

    def retrieveSnopesData(self):
        pass

    def classifyTweets(self, username, file):
        pass

    def tagTweet(self, username, tweet, isFake):
        pass

    def retrieveFakeNewsData(self):
        pass

    def register(self, username, password):
        pass

    def login(self, username, password):
        pass

    def deleteUser (self, admin_username, username_to_delete):
        pass

    def viewUserSearchHistory (self, username, username_to_view):
        pass

    def configClassifier(self, username, classifier, configuration):
        pass

    def editTwittersTokens(self, username, tokens):
        pass