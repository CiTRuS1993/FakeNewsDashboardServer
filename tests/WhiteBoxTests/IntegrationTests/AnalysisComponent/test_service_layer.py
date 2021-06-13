import unittest

import mock as mock

from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface
from unittest import TestCase, mock

from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager.TestsObjects import AnalysedTweet, name, Claim


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis_manager = AnalysisManagerInterface()
        self.tweet1 =  {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 =  {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 =  {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.claims = {'claim1': {'1': self.tweet1, '3': self.tweet3},
                       'claim2': {'1': self.tweet1, '2': self.tweet2}}
        self.analysed_tweet1 = AnalysedTweet('1', name('aa'), 'tweet1', 'Happy', 2, 1)
        self.analysed_tweet2 = AnalysedTweet('2', name('aa'), 'tweet2', 'Sad', -1, 0)
        self.analysed_tweet3 = AnalysedTweet('3', name('aa'), 'tweet3', 'Sad', -3, 1)
        self.analysed_tweets = [self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3]
        self.trends_topics = [
                              Claim('claim1', [self.analysed_tweet1, self.analysed_tweet2], 1),
                              Claim('claim2', [self.analysed_tweet2, self.analysed_tweet3], 2),
                              Claim('claim3', [self.analysed_tweet1, self.analysed_tweet2], 3),
                              Claim('claim4', [self.analysed_tweet1, self.analysed_tweet3], 4),
                              Claim('some claim',[self.analysed_tweet1, self.analysed_tweet2, self.analysed_tweet3], 5)
                                ]
        self.temp = [1, 1, 0]
        self.sentiment = [1, 1, 0]


    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getGoogleTrendsStatistics(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.getGoogleTrendsStatistics.return_value = self.analysed_tweets
        res= self.analysis_manager.getGoogleTrendsStatistics()
        self.assertEqual(self.analysed_tweets, res)


    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getSnopesStatistics(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.getSnopesStatistics.return_value = self.analysed_tweets
        res= self.analysis_manager.getSnopesStatistics()
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classifyTrends(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.getGoogleTrendsStatistics.return_value = self.analysed_tweets
        res= self.analysis_manager.getGoogleTrendsStatistics()
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_classifySnopes(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.getSnopesStatistics.return_value = self.analysed_tweets
        res= self.analysis_manager.classifySnopes(self.claims)
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getTemperature(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.getTemperature.return_value = self.temp
        res = self.analysis_manager.getTemperature()
        self.assertEqual(self.temp, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotions(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.get_emotions.return_value = ['Happy', 'Sad']
        res = self.analysis_manager.get_emotions()
        self.assertEqual(['Happy', 'Sad'], res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_sentiment(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.get_sentiment.return_value = self.sentiment
        res = self.analysis_manager.get_sentiment()
        self.assertEqual(self.sentiment, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topic(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.get_topic.return_value = self.analysed_tweets
        res = self.analysis_manager.get_topic(1)
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotion_tweets(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.get_emotion_tweets.return_value = self.analysed_tweets
        res = self.analysis_manager.get_emotion_tweets('Sad')
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topics(self, mock):
        self.analysis_manager.analysisManagerLogic = mock
        mock.get_topics.return_value = self.trends_topics
        res = self.analysis_manager.get_topics(1)
        self.assertEqual(self.trends_topics, res)


if __name__ == '__main__':
    unittest.main()
