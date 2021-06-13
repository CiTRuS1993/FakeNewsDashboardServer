import unittest

from BuisnessLayer.AnalysisManager.DataObjects import Temperature, Sentiment
from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis_manager = AnalysisManagerInterface()
        self.tweet1 =  {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 =  {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 =  {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.claims = {'claim1': {'1': self.tweet1, '3': self.tweet3},
                       'claim2': {'1': self.tweet1, '2': self.tweet2}}

    def test_getGoogleTrendsStatistics(self):
        res= self.analysis_manager.getGoogleTrendsStatistics()
        self.assertTrue(len(res)>0) # no data

    def test_getSnopesStatistics(self):
        res= self.analysis_manager.getSnopesStatistics()
        self.assertTrue(len(res)>0)

    def test_classifyTrends(self):
        res= self.analysis_manager.getGoogleTrendsStatistics()
        self.assertTrue(len(res)>0)  # no data

    def test_classifySnopes(self):
        res= self.analysis_manager.classifySnopes(self.claims)
        self.assertTrue(len(res)>0)

    def test_getTemperature(self):
        res = self.analysis_manager.getTemperature()
        self.assertTrue(type(res)==Temperature)

    def test_get_emotions(self):
        def is_emotion (dict):
            emotions = ['Happy', 'Sad', 'Surprise', 'Angry', 'Fear']
            for emotion_dict in dict['emotions']: # dict['emotions'] is type of list
                if emotion_dict['label'] not in emotions:
                    return False
            return True

        res = self.analysis_manager.get_emotions()
        self.assertTrue(len(res) > 0)
        self.assertTrue(is_emotion(res))

    def test_get_sentiment(self):
        res = self.analysis_manager.get_sentiment()
        self.assertTrue(type(res)==Sentiment)

    def test_get_topic(self):
        res = self.analysis_manager.get_topic(1)
        self.assertTrue(len(res) > 0)

    def test_get_emotion_tweets(self):
        res = self.analysis_manager.get_emotion_tweets('Sad')
        self.assertTrue(len(res) > 0)  # not collects data, so there are no topics

    def test_get_topics(self):
        res = self.analysis_manager.get_topics(1)
        self.assertTrue(len(res) > 0)  # not collects data, so there are no topics


if __name__ == '__main__':
    unittest.main()
