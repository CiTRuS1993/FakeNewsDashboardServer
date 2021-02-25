from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager


class AnalysisManagerInterface:

    def __init__(self):
        self.analysisManagerLogic=AnalysisManager()

    def getGoogleTrendsStatistics(self):
        return self.analysisManagerLogic.getGoogleTrendsStatistics()

    def getSnopesStatistics(self):
        pass

    def classifyTweets(self, file):
        pass

    def retrieveFakeNewsData(self):
        return self.analysisManagerLogic.retrieveFakeNewsData()

    def configClassifier(self, classifier, configuration):
        pass

    def classifyTrends(self, trends_tweets):
        return self.analysisManagerLogic.classifyTrends(trends_tweets)

    def classifySnopes(self, claims):
        pass

    def tagTweets(self, tweet_id, isFake):
        pass

