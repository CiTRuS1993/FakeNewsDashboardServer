import unittest
from unittest import mock

from ServiceLayer.DashboardFacade import DashboardFacade
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager.TestsObjects import AnalysedTweet, name, Claim


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dashboard = DashboardFacade("username", "123")
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
    def test_googleTrendsStatistics(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.getGoogleTrendsStatistics.return_value = self.analysed_tweets
        res= self.dashboard.googleTrendsStatistics()
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_snopesStatistics(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.getSnopesStatistics.return_value = self.analysed_tweets
        res= self.dashboard.snopesStatistics()
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade")
    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_retrieveGoogleTrendsData(self, analysis_manager, external_mock):
        self.dashboard.analysisManager.analysisManagerLogic = analysis_manager
        analysis_manager.getGoogleTrendsStatistics.return_value = self.analysed_tweets
        self.dashboard.externalSystemsManager.extrenalManagerLogic = external_mock
        res= self.dashboard.retrieveGoogleTrendsData()
        self.assertEqual(self.analysed_tweets, res)


    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade")
    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_retrieveSnopesData(self, analysis_mock, external_mock):
        self.dashboard.analysisManager.analysisManagerLogic = analysis_mock
        analysis_mock.getSnopesStatistics.return_value = self.analysed_tweets
        self.dashboard.externalSystemsManager.extrenalManagerLogic = external_mock
        # external_mock.retrieveSnopesData.return_value = self.claims
        res= self.dashboard.retrieveSnopesData()
        self.assertEqual(self.analysed_tweets, res)


    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_getTemperature(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.getTemperature.return_value = self.temp
        res = self.dashboard.getTemperature()
        self.assertEqual(self.temp, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotions(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.get_emotions.return_value = ['Happy', 'Sad']
        res = self.dashboard.get_emotions()
        self.assertEqual(['Happy', 'Sad'], res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_sentiment(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.get_sentiment.return_value = self.sentiment
        res = self.dashboard.get_sentiment()
        self.assertEqual(self.sentiment, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topic(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.get_topic.return_value = self.analysed_tweets
        res = self.dashboard.get_topic(1)
        self.assertEqual(self.analysed_tweets, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_topics(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.get_topics.return_value = self.trends_topics
        res = self.dashboard.get_topics(1)
        self.assertEqual(self.trends_topics, res)

    @mock.patch("BuisnessLayer.AnalysisManager.AnalysisManager")
    def test_get_emotion_tweets(self, mock):
        self.dashboard.analysisManager.analysisManagerLogic = mock
        mock.get_emotion_tweets.return_value = self.analysed_tweets
        res = self.dashboard.get_emotion_tweets('Sad')
        self.assertEqual(self.analysed_tweets, res)


    # # ----------------------------------- Users Options ------------------------------------------

    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade")
    def test_searchTweetsByKeywords(self, mock):
        self.dashboard.externalSystemsManager.extrenalManagerLogic = mock
        # mock.get_emotion_tweets.return_value = self.analysed_tweets
        res = self.dashboard.searchTweetsByKeywords('username', 'keywords')
        self.assertEqual(True, res)
        res = self.dashboard.searchTweetsByKeywords('user', 'keywords')
        self.assertEqual(False, res)

    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade")
    def test_editTwittersTokens(self, mock):
        self.dashboard.externalSystemsManager.extrenalManagerLogic = mock
        mock.edit_twitters_tokens.return_value = True
        res = self.dashboard.editTwittersTokens('username', 'keywords')
        self.assertEqual(True, res)
        res = self.dashboard.editTwittersTokens('user', 'keywords')
        self.assertEqual(False, res)

    # # ----------------------------------- Manage Users --------------------------------------------

    @mock.patch("BuisnessLayer.Users.UsersManagerFacade")
    def test_register(self, mock):
        self.dashboard.usersManager.userManagerLogic = mock
        mock.register.return_value = False
        res = self.dashboard.register('username', 'pass')
        self.assertEqual(False, res)
        mock.register.return_value = True
        res = self.dashboard.register('user', '123')
        self.assertEqual(True, res)

    @mock.patch("BuisnessLayer.Users.UsersManagerFacade")
    def test_login(self, mock):
        self.dashboard.usersManager.userManagerLogic = mock
        mock.login.return_value = False
        res = self.dashboard.login('username', 'pass')
        self.assertEqual(False, res)
        mock.login.return_value = True
        res = self.dashboard.login('user', '123')
        self.assertEqual(True, res)

    @mock.patch("BuisnessLayer.Users.UsersManagerFacade")
    def test_deleteUser(self, mock):
        self.dashboard.usersManager.userManagerLogic = mock
        mock.delete_user.return_value = False
        res = self.dashboard.deleteUser('username', 'pass')
        self.assertEqual(False, res)
        mock.delete_user.return_value = True
        res = self.dashboard.deleteUser('user', '123')
        self.assertEqual(True, res)

if __name__ == '__main__':
    unittest.main()
