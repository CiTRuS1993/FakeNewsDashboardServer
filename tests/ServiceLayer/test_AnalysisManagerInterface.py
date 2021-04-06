import unittest

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager
from tests.buisnessLayer.AnalysisManager.TestsObjects import AnalysedTweet, Name


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis_manager= AnalysisManager()
        self.snopes = {'claim1': set(['tweet1', 'tweet2','tweet3']),
                       'claim2': set(['tweet1', 'tweet2','tweet3']),
                       'claim3': set(['tweet1', 'tweet2','tweet3'])}
        self.analysed_tweets = {}
        self.analysed_tweet1 = AnalysedTweet('1', Name('aa'), 'tweet1', 'happy', 2, '0')
        self.analysed_tweet2 = AnalysedTweet('2', Name('aa'), 'tweet2', 'sad', -1, '1')
        self.analysed_tweet3 = AnalysedTweet('3', Name('aa'), 'tweet3', 'sad', -3, '0')
        self.analysed_tweets = {
            '1': {'id': 1, 'keyword': 'Donald Trump',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)},
            '2': {'id': 2, 'keyword': 'Covid19',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)},
            '3': {'id': 3, 'keyword': 'Elections',
                  'tweets': (self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3)}}

    # def getGoogleTrendsStatistics(self):
    #     return self.analysisManagerLogic.getGoogleTrendsStatistics()
    #
    # def getSnopesStatistics(self):
    #     return self.analysisManagerLogic.getSnopesStatistics()
    #
    # def classifyTweets(self, file):
    #     return self.analysisManagerLogic.classifyTweets(file)
    #
    # def retrieveFakeNewsData(self):
    #     return self.analysisManagerLogic.retrieveFakeNewsData()
    #
    # def configClassifier(self, classifier, configuration):
    #     return self.analysisManagerLogic.configClassifier(classifier, configuration)
    #
    # def classifyTrends(self, trends_tweets):
    #     self.analysisManagerLogic.classifyTrends(trends_tweets)
    #     return self.analysisManagerLogic.getGoogleTrendsStatistics()
    #
    # def classifySnopes(self, claims_tweets):
    #     self.analysisManagerLogic.classifySnopes(claims_tweets)
    #     return self.analysisManagerLogic.getSnopesStatistics()
    #
    # # TODO
    # def tagTweets(self, tweet_id, isFake):
    #     # return self.analysisManagerLogic.tagTweets(tweet_id, isFake)
    #     # Yarin- maybe just add it to the ORM from here? does it have to pass throw the analysisManagerLogic?
    #     pass
    #
    # def getTemperature(self):
    #     return self.analysisManagerLogic.getTemperature()
    #
    # def get_emotions(self):
    #     return self.analysisManagerLogic.get_emotions()
    #
    # def get_sentiment(self):
    #     return self.analysisManagerLogic.get_sentiment()
    #
    # def get_topic(self, topic_id):
    #     return self.analysisManagerLogic.get_topic(topic_id)
    #
    # def get_emotion_tweets(self, emotion):
    #     return self.analysisManagerLogic.get_emotion_tweets(emotion)


    def test_getGoogleTrendsStatistics(self):
        self.assertEqual(True, False)

    def test_getSnopesStatistics(self):
        self.assertEqual(True, False)

    def test_classifyTweets(self):
        self.assertEqual(True, False)

    def test_retrieveFakeNewsData(self):
        self.assertEqual(True, False)

    def test_configClassifier(self):
        self.assertEqual(True, False)

    def test_classifyTrends(self):
        self.assertEqual(True, False)

    def test_classifySnopes(self):
        self.assertEqual(True, False)

    def test_tagTweets(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
