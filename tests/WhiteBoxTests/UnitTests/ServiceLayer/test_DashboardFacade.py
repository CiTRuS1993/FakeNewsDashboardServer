import time
import unittest

import mock as mock

from ServiceLayer.DashboardFacade import DashboardFacade
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager import AnalysedTweet, Name


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
        self.temp = []
        self.emotions = []
        self.sentiment = []


    # ------------------------------- Retrieve Data & External Systems -----------------------------

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveFakeNewsData(self,  mock_analysis):  # returns statistics
        self.dashboard.analysisManager= mock_analysis
        ret = {'TODO': 'why am I doing it???'}
        mock_analysis.retrieveFakeNewsData.return_value = ret
        self.assertEqual(self.dashboard.retrieveFakeNewsData(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_googleTrendsStatistics(self, mock):  # returns statistics
        self.dashboard.analysisManager= mock
        ret = self.analysed_tweets
        mock.getGoogleTrendsStatistics.return_value = ret
        self.assertEqual(self.dashboard.googleTrendsStatistics(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_snopesStatistics(self, mock):  # returns statistics
        self.dashboard.analysisManager= mock
        ret = self.snopes
        mock.getSnopesStatistics.return_value = ret
        self.assertEqual(self.dashboard.snopesStatistics(), ret)

    # @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveGoogleTrendsData(self):
        time.sleep(4)
        self.dashboard.retrieveGoogleTrendsData()
        time.sleep(4)
        print(self.dashboard.retrieveFakeNewsData())

    @mock.patch("ServiceLayer.ExternalSystemsAPIsManagerInterface")
    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_retrieveSnopesData(self, mock_analysis, mock_external):
        self.dashboard.analysisManager= mock_analysis
        self.dashboard.externalSystemsManager= mock_external
        ret = self.snopes
        mock_analysis.classifySnopes.return_value = ret
        mock_external.retrieveSnopesData.return_value = self.claims
        self.assertEqual(self.dashboard.retrieveSnopesData(), ret)

    @mock.patch("ServiceLayer.UsersManagerInterface")
    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_configClassifier(self, mock_analysis, mock_users):
        self.dashboard.analysisManager = mock_analysis
        self.dashboard.usersManager = mock_users
        ret = True
        mock_analysis.configClassifier.return_value = ret
        mock_users.is_admin.return_value = True
        self.assertEqual(self.dashboard.configClassifier('username', 'classifier1', 'configuration'), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_getTemperature(self, mock_analysis):
        self.dashboard.analysisManager = mock_analysis
        ret = self.temp
        mock_analysis.getTemperature.return_value = ret
        self.assertEqual(self.dashboard.getTemperature(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_get_emotions(self, mock_analysis):
        self.dashboard.analysisManager = mock_analysis
        ret = self.emotions
        mock_analysis.get_emotions.return_value = ret
        self.assertEqual(self.dashboard.get_emotions(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_get_sentiment(self, mock_analysis):
        self.dashboard.analysisManager = mock_analysis
        ret = self.sentiment
        mock_analysis.get_sentiment.return_value = ret
        self.assertEqual(self.dashboard.get_sentiment(), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_get_topic(self, mock_analysis):
        self.dashboard.analysisManager = mock_analysis
        ret = {'tweets': self.analysed_tweets, 'emotions': self.emotions}
        mock_analysis.get_topic.return_value = ret
        self.assertEqual(self.dashboard.get_topic(1), ret)

    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_get_emotion_tweets(self, mock_analysis):
        self.dashboard.analysisManager = mock_analysis
        ret = self.analysed_tweets
        mock_analysis.get_emotion_tweets.return_value = ret
        self.assertEqual(self.dashboard.get_emotion_tweets('happy'), ret)

    # ----------------------------------- Users Options ------------------------------------------

    @mock.patch("ServiceLayer.ExternalSystemsAPIsManagerInterface")
    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_searchTweetsByKeywords(self, mock_users, mock_external):
        self.dashboard.externalSystemsManager = mock_external
        self.dashboard.usersManager = mock_users
        ret = True
        mock_external.searchTweetsByKeywords.return_value = 1
        mock_users.userExists.return_value = ret
        self.assertEqual(self.dashboard.searchTweetsByKeywords('username', 'keywords'), ret)

    #
    # def tagTweet(self, username, tweet_id, isFake):
    #     if self.usersManager.userExists(username):
    #         self.analysisManager.tagTweets(tweet_id, isFake)
    #         self.usersManager.tagTweet(username, tweet_id)
    #

    # @mock.patch("ServiceLayer.UsersManagerInterface")
    # @mock.patch("ServiceLayer.AnalysisManagerInterface")
    # def test_tagTweet(self, mock_analysis, mock_users):
    #     self.dashboard.analysisManager = mock_analysis
    #     self.dashboard.usersManager = mock_users
    #     ret = True
    #     mock_users.tagTweet.return_value = ret
    #     mock_users.userExists.return_value = True
    #     self.assertEqual(self.dashboard.tagTweet('username', '1223234', '1'), ret)
    #

    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_viewUserSearchHistory(self, mock):
        self.dashboard.usersManager = mock
        ret = [1,5,12]
        mock.viewUserSearchHistory.return_value = ret
        self.assertEqual(self.dashboard.viewUserSearchHistory('username1', 'username2'), ret)

    @mock.patch("ServiceLayer.ExternalSystemsAPIsManagerInterface")
    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_editTwittersTokens(self, mock_users, mock_external):
        self.dashboard.externalSystemsManager = mock_external
        self.dashboard.usersManager = mock_users
        ret = True
        mock_external.editTwittersTokens.return_value = ret
        mock_users.is_admin.return_value = True
        self.assertEqual(self.dashboard.editTwittersTokens('username', ['token1', 'token2']), ret)

    @mock.patch("ServiceLayer.UsersManagerInterface")
    @mock.patch("ServiceLayer.AnalysisManagerInterface")
    def test_classifyTweets(self, mock_analysis, mock_users):
        self.dashboard.analysisManager = mock_analysis
        self.dashboard.usersManager = mock_users
        ret = True
        mock_users.classifyTweets.return_value = ret
        mock_users.userExists.return_value = True
        self.assertEqual(self.dashboard.classifyTweets('username', 'file_dir'), ret)
        ret = False
        mock_users.classifyTweets.return_value = ret
        mock_users.userExists.return_value = False
        self.assertEqual(self.dashboard.classifyTweets('username', 'file_dir'), ret)

    # ----------------------------------- Manage Users --------------------------------------------

    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_register(self, mock):
        self.dashboard.usersManager = mock
        ret = True
        mock.register.return_value = ret
        self.assertEqual(self.dashboard.register('username', '12345'), ret)

    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_login(self, mock):
        self.dashboard.usersManager = mock
        ret = True
        mock.login.return_value = ret
        self.assertEqual(self.dashboard.login('username', '12345'), ret)

    @mock.patch("ServiceLayer.UsersManagerInterface")
    def test_deleteUser(self, mock):
        self.dashboard.usersManager = mock
        ret = True
        mock.deleteUser.return_value = ret
        self.assertEqual(self.dashboard.deleteUser('admin_username', 'user_to_delete'), ret)

if __name__ == '__main__':
    unittest.main()
