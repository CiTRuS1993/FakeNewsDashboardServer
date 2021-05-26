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

    def tagTweets(self, tweet_id, isFake):
        # return self.analysisManagerLogic.tagTweets(tweet_id, isFake)
        # maybe just add it to the ORM from here? does it have to pass throw the analysisManagerLogic?
        pass

    def getTemperature(self):
        return self.analysisManagerLogic.getTemperature()

    def get_emotions(self):
        return self.analysisManagerLogic.get_emotions()

    def get_sentiment(self):
        return self.analysisManagerLogic.get_sentiment()

    def get_topic(self, topic_id):
        return self.analysisManagerLogic.get_topic(topic_id)

    def get_emotion_tweets(self, emotion):
        return self.analysisManagerLogic.get_emotion_tweets(emotion)
