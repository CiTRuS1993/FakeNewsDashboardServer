import time
from unittest import TestCase

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager


class TestAnalysisManager(TestCase):
    def setUp(self) -> None:
        self.analysisManager = AnalysisManager()
        self.trends = ['Donald Trump', 'Covid19', 'Elections']
        self.tweet1 = {'id': '1', 'author':'aa', 'content': 'tweet1'}
        self.tweet2 = {'id': '2', 'author':'aa', 'content': 'tweet2'}
        self.tweet3 = {'id': '3', 'author':'aa', 'content': 'tweet3'}
        self.trends_tweets = {'Donald Trump':{'id': 1, 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
                              'Covid19': {'id': 2, 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}},
                              'Elections': {'id': 3, 'tweets':{'1': self.tweet1, '2': self.tweet2, '3': self.tweet3}}}
        self.claims = ['claim1', 'claim2', 'claim3']
        self.snopes = {'claim1': [self.tweet1, self.tweet2, self.tweet3],
                       'claim2': [self.tweet1, self.tweet2, self.tweet3],
                       'claim3': [self.tweet1, self.tweet2, self.tweet3]}

    def test_classify_trends(self):
        self.assertEqual({}, self.analysisManager.getGoogleTrendsStatistics())
        # amount = len(self.analysisManager.dashboard_statistics.keys())
        self.assertTrue(self.analysisManager.classifyTrends(self.trends_tweets))
        time.sleep(10)
        # print(self.analysisManager.getGoogleTrendsStatistics())
        self.assertTrue(len(self.analysisManager.getGoogleTrendsStatistics().keys()) > 0)
        # self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)


    def test_classify_snopes(self):
        self.assertEqual({}, self.analysisManager.getSnopesStatistics())
        # amount = len(self.analysisManager.dashboard_statistics())
        self.analysisManager.classifySnopes(self.snopes)
        time.sleep(10)
        self.assertTrue(len(self.analysisManager.getSnopesStatistics()) > 0)
        # self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)

    def test_get_claims_from_trend(self):
        for trend in self.trends_tweets:
            self.assertTrue(len(self.analysisManager.get_claims_from_trend(self.trends_tweets[trend]['tweets'])) > 0)

    def test_get_tweets_by_emotion(self):
        self.analysisManager.classifyTrends(self.trends_tweets)
        time.sleep(10)
        emotion = self.analysisManager.getGoogleTrendsStatistics()['Donald Trump']['statistics']['emotion'][0]
        # print(emotion)
        # print(self.analysisManager.get_emotion_tweets(emotion))
        self.assertTrue(len(self.analysisManager.get_emotion_tweets(emotion))>0)

# TODO

#     def test_classify_tweets(self):
#         self.fail()
#
#     def test_config_classifier(self):
#         self.fail()