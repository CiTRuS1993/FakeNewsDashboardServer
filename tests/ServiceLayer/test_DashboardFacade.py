import time
import unittest

import mock as mock

from ServiceLayer.DashboardFacade import DashboardFacade
from tests.buisnessLayer.AnalysisManager.TestsObjects import AnalysedTweet, Name


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dashboard = DashboardFacade("username", "123")
        self.snopes = {'claim1': set(['tweet1', 'tweet2', 'tweet3']),
                       'claim2': set(['tweet1', 'tweet2', 'tweet3']),
                       'claim3': set(['tweet1', 'tweet2', 'tweet3'])}
        self.claims = ['claim1', 'claim2', 'claim3']
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

        #
        # def configClassifier(self, username, classifier, configuration):
        #     if self.usersManager.is_admin(username):
        #         return self.analysisManager.configClassifier(classifier, configuration)
        #     return False  # TODO- exception?
        #
        # def getTemperature(self):
        #     return self.analysisManager.getTemperature()
        #
        # def get_emotions(self):
        #     return self.analysisManager.get_emotions()
        #
        # def get_sentiment(self):
        #     return self.analysisManager.get_sentiment()
        #
        # def get_topic(self, topic_id):
        #     return self.analysisManager.get_topic(topic_id)
        #
        # def get_emotion_tweets(self, emotion):
        #     return self.analysisManager.get_emotion_tweets(emotion)

    # ------------------------------- Retrieve Data & External Systems -----------------------------

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveFakeNewsData(self, mock):  # returns statistics
        ret = {'TODO': 'why am I doing it???'}
        mock.retrieveFakeNewsData.return_value = ret
        self.assertEqual(self.dashboard.retrieveFakeNewsData(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_googleTrendsStatistics(self, mock):  # returns statistics
        ret = self.analysed_tweets
        mock.getGoogleTrendsStatistics.return_value = ret
        self.assertEqual(self.dashboard.googleTrendsStatistics(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_snopesStatistics(self, mock):  # returns statistics
        ret = self.snopes
        mock.getSnopesStatistics.return_value = ret
        self.assertEqual(self.dashboard.snopesStatistics(), ret)

        # TODO?

    # @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveGoogleTrendsData(self):
        time.sleep(4)
        self.dashboard.retrieveGoogleTrendsData()
        time.sleep(4)
        print(self.dashboard.retrieveFakeNewsData())

    @mock.patch("ServiceLayer.ExternalSystemsAPIsManagerInterface")
    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveSnopesData(self, mock_analysis, mock_external):
        ret = self.snopes
        mock_analysis.orm = mock.Mock()
        mock_analysis.classifySnopes.return_value = ret
        mock_external.retrieveSnopesData.return_value = self.claims
        mock_external.extrenalManagerLogic = mock.Mock()
        self.assertEqual(self.dashboard.retrieveSnopesData(), ret)

    def test_configClassifier(self):
        self.assertEqual(True, False)

    # ----------------------------------- Users Options ------------------------------------------

    #
    # def searchTweetsByKeywords(self, username, keyword, token=None):
    #     if (self.usersManager.userExists(username)):
    #         search_id = self.externalSystemsManager.searchTweetsByKeywords(keyword, token)
    #         self.usersManager.saveSearchTweetsByKeywords(username, search_id)
    #         return True
    #     return False
    #
    # def tagTweet(self, username, tweet_id, isFake):
    #     if self.usersManager.userExists(username):
    #         self.analysisManager.tagTweets(tweet_id, isFake)
    #         self.usersManager.tagTweet(username, tweet_id)
    #         # TODO- what to return?
    #
    # def viewUserSearchHistory(self, username, username_to_view):
    #     return self.usersManager.viewUserSearchHistory(username, username_to_view)
    #
    # def editTwittersTokens(self, username, tokens):
    #     if self.usersManager.is_admin(username):
    #         return self.externalSystemsManager.editTwittersTokens(tokens)
    #     return False  # TODO- exception?
    #
    # def classifyTweets(self, username, file):
    #     if (self.usersManager.userExists(username)):
    #         classify_id = self.analysisManager.classifyTweets(file)
    #         return self.usersManager.classifyTweets(username, classify_id)
    #     return False  # TODO- exception?
    #
    def test_searchTweetsByKeywords(self):
        self.assertEqual(True, False)

    def test_tagTweet(self):
        self.assertEqual(True, False)

    def test_viewUserSearchHistory(self):
        self.assertEqual(True, False)

    def test_editTwittersTokens(self):
        self.assertEqual(True, False)

    def test_classifyTweets(self):
        self.assertEqual(True, False)

    # ----------------------------------- Manage Users --------------------------------------------

    # def register(self, username, password):
    #     return self.usersManager.register(username, password)
    #
    # def login(self, username, password):
    #     return self.usersManager.login(username, password)
    #
    # def deleteUser(self, admin_username, username_to_delete):
    #     return self.usersManager.deleteUser(admin_username, username_to_delete)
    #
    def test_register(self):
        self.assertEqual(True, False)

    def test_login(self):
        self.assertEqual(True, False)

    def test_deleteUser(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
