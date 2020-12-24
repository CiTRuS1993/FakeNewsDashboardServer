from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager


class AnalysisManagerInterface:

    def __init__(self):
        self.analysisManagerLogic=AnalysisManager()

    def getGoogleTrendsStatistics(self):
        pass

    def getSnopesStatistics(self):
        pass

    def classifyTweets(self, file):
        pass

    def retrieveFakeNewsData(self):
        pass

    def configClassifier(self, classifier, configuration):
        pass

    def classifyTrends(self, trends):
        pass

    def classifySnopes(self, claims):
        pass

    def tagTweets(self, tweet_id, isFake):
        pass

