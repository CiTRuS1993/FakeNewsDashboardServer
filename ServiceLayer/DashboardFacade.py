from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface
from ServiceLayer.UsersManagerInterface import UsersManagerInterface
import threading

class DashboardFacade:

    def __init__(self, username, password):
        self.analysisManager=AnalysisManagerInterface()
        self.externalSystemsManager=ExternalSystemsAPIsManagerInterface()
        self.usersManager=UsersManagerInterface(username, password)
        self.trends_timer = threading.Timer(12.0*60, self.retrieveGoogleTrendsData)
        self.snopes_timer = threading.Timer(12.0*60, self.retrieveSnopesData)


# ------------------------------- Retrieve Data & External Systems -----------------------------

# search tweets
    # gets all data related to the dashboard
    def retrieveFakeNewsData(self):
        return self.analysisManager.retrieveFakeNewsData()

    # gets all data related to the Google Trends window
    def googleTrendsStatistics(self):
        return self.analysisManager.getGoogleTrendsStatistics()

    # gets all data related to the Snopes window
    def snopesStatistics(self):
        return self.analysisManager.getSnopesStatistics()

    # each 12 hours retrieve the new Google Trends topics
    def retrieveGoogleTrendsData(self):
        new_trends= self.externalSystemsManager.retrieveGoogleTrendsData()
        self.analysisManager.classifyTrends(new_trends)

    # each 12 hours retrieve the new Snopes claims
    def retrieveSnopesData(self):
        new_claims= self.externalSystemsManager.retrieveSnopesData()
        self.analysisManager.classifySnopes(new_claims)

    def configClassifier(self, username, classifier, configuration):
        if self.usersManager.is_admin(username):
            return self.analysisManager.configClassifier(classifier, configuration)
        return False #TODO- exception?

# ----------------------------------- Users Options ------------------------------------------

    def searchTweetsByKeywords(self, username, keyword, token=None):
        if (self.usersManager.userExists(username)):
            search_id= self.externalSystemsManager.searchTweetsByKeywords(keyword, token)
            self.usersManager.saveSearchTweetsByKeywords(username, search_id)
            return True
        return False

    def tagTweet(self, username, tweet, isFake):
        if (self.usersManager.userExists(username)):
            # TODO - analysis?
            pass

    def viewUserSearchHistory (self, username, username_to_view):
        return self.usersManager.viewUserSearchHistory(username,username_to_view)

    def editTwittersTokens(self, username, tokens):
        if self.usersManager.is_admin(username):
            self.externalSystemsManager.editTwittersTokens(tokens)

    def classifyTweets(self, username, file):
        #TODO
        pass

# ----------------------------------- Manage Users --------------------------------------------

    def register(self, username, password):
        self.usersManager.register(username,password)

    def login(self, username, password):
        self.usersManager.login(username,password)

    def deleteUser(self, admin_username, username_to_delete):
        self.usersManager.deleteUser(admin_username, username_to_delete)


