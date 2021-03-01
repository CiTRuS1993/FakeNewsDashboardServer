from unittest import TestCase

from BuisnessLayer.AnalysisManager.AnalysisManager import AnalysisManager


class TestAnalysisManager(TestCase):
    def setUp(self) -> None:
        self.analysisManager = AnalysisManager()
        self.trends = ['Donald Trump', 'Covid19', 'Elections']
        self.trends_tweets = {'Donald Trump': set(['tweet1', 'tweet2', 'tweet3']),
                              'Covid19': set(['tweet1', 'tweet2', 'tweet3']),
                              'Elections': set(['tweet1', 'tweet2', 'tweet3'])}
        self.claims = ['claim1', 'claim2', 'claim3']
        self.snopes = {'claim1': set(['tweet1', 'tweet2', 'tweet3']),
                       'claim2': set(['tweet1', 'tweet2', 'tweet3']),
                       'claim3': set(['tweet1', 'tweet2', 'tweet3'])}

    def test_classify_trends(self):
        self.assertEqual({}, self.analysisManager.getGoogleTrendsStatistics())
        amount = len(self.analysisManager.dashboard_statistics.keys())
        self.assertTrue(self.analysisManager.classifyTrends(self.trends_tweets))
        # print(self.analysisManager.getGoogleTrendsStatistics())
        self.assertTrue(len(self.analysisManager.getGoogleTrendsStatistics().keys()) > 0)
        self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)


    def test_classify_snopes(self):
        self.assertEqual({}, self.analysisManager.getSnopesStatistics())
        amount = len(self.analysisManager.dashboard_statistics())
        self.assertTrue(len(self.analysisManager.classifySnopes(self.snopes)) > 0)
        self.assertTrue(len(self.analysisManager.getSnopesStatistics()) > 0)
        self.assertTrue(len(self.analysisManager.dashboard_statistics()) > amount)

    def test_get_claims_from_trend(self):
        self.assertTrue(len(self.analysisManager.get_claims_from_trend(self.trends)) > 0)

# TODO

#     def test_classify_tweets(self):
#         self.fail()
#
#     def test_config_classifier(self):
#         self.fail()