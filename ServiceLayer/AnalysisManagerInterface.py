from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager


class AnalysisManagerInterface:

    def __init__(self):
        self.analysisManagerLogic=AnalysisManager()

    def getGoogleTrendsStatistics(self):
        return self.analysisManagerLogic.getGoogleTrendsStatistics()

    def getSnopesStatistics(self):
        return self.analysisManagerLogic.getSnopesStatistics()

    def classifyTweets(self, file):
        return self.analysisManagerLogic.classifyTweets(file)

    def retrieveFakeNewsData(self):
        return self.analysisManagerLogic.retrieveFakeNewsData()

    def configClassifier(self, classifier, configuration):
        return self.analysisManagerLogic.configClassifier(classifier, configuration)

    def classifyTrends(self, trends_tweets):
        self.analysisManagerLogic.classifyTrends(trends_tweets)
        return self.analysisManagerLogic.getGoogleTrendsStatistics()

    def classifySnopes(self, claims_tweets):
        self.analysisManagerLogic.classifySnopes(claims_tweets)
        return self.analysisManagerLogic.getSnopesStatistics()

    # TODO
    def tagTweets(self, tweet_id, isFake):
        # return self.analysisManagerLogic.tagTweets(tweet_id, isFake)
        # Yarin- maybe just add it to the ORM from here? does it have to pass throw the analysisManagerLogic?
        pass

