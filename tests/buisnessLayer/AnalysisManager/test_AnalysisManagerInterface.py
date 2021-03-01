from unittest import TestCase
from ServiceLayer.AnalysisManagerInterface import AnalysisManagerInterface


class TestAnalysisManagerInterface(TestCase):
    def setUp(self) -> None:
        self.analysisManager = AnalysisManagerInterface()
        self.trends = ['Donald Trump', 'Covid19', 'Elections']
        self.trends_tweets = {'Donald Trump': set(['tweet1', 'tweet2','tweet3']),
                              'Covid19': set(['tweet1', 'tweet2','tweet3']),
                              'Elections': set(['tweet1', 'tweet2','tweet3'])}
        self.claims = ['claim1', 'claim2', 'claim3']
        self.snopes = {'claim1': set(['tweet1', 'tweet2','tweet3']),
                       'claim2': set(['tweet1', 'tweet2','tweet3']),
                       'claim3': set(['tweet1', 'tweet2','tweet3'])}

# TODO -  integration
    def test_classify_trends(self):
        self.assertEqual([], self.analysisManager.getGoogleTrendsStatistics())
        # self.assertEqual(self.claims, self.analysisManager.classifyTrends(self.trends_tweets))
        self.assertTrue(len(self.analysisManager.classifyTrends(self.trends_tweets))>0)

    def test_classify_snopes(self):
        self.fail()


    # TODO

    # def test_classify_tweets(self):
    #     self.fail()

    # def test_config_classifier(self):
    #     self.fail()

    # def test_tag_tweets(self):
    #     self.fail()
