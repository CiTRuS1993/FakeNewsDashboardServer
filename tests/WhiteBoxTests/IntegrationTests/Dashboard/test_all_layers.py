import unittest

from BuisnessLayer.AnalysisManager.DataObjects import Temperature, Sentiment
from ServiceLayer.DashboardFacade import DashboardFacade
from tests.WhiteBoxTests.UnitTests.buisnessLayer.AnalysisManager.TestsObjects import AnalysedTweet, name, Claim


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dashboard = DashboardFacade("username", "123")

    def test_googleTrendsStatistics(self):
        if (len(self.dashboard.googleTrendsStatistics()) == 0):
            self.dashboard.retrieveGoogleTrendsData()
        res= self.dashboard.googleTrendsStatistics()
        self.assertTrue(len(res)>0)

    def test_snopesStatistics(self):
        res= self.dashboard.snopesStatistics()
        self.assertTrue(len(res)>0)

    def test_retrieveGoogleTrendsData(self):
        res= self.dashboard.retrieveGoogleTrendsData()
        self.assertTrue(len(res)>0)

    def test_retrieveSnopesData(self):
        res= self.dashboard.retrieveSnopesData()
        self.assertTrue(len(res)>0)

    def test_getTemperature(self):
        res = self.dashboard.getTemperature()
        self.assertTrue(type(res)==Temperature)

    def test_get_emotions(self):
        def is_emotion (dict):
            emotions = ['Happy', 'Sad', 'Surprise', 'Angry', 'Fear']
            for emotion_dict in dict['emotions']: # dict['emotions'] is type of list
                if emotion_dict['label'] not in emotions:
                    return False
            return True

        res = self.dashboard.get_emotions()
        self.assertTrue(len(res)>0)
        self.assertTrue(is_emotion(res))

    def test_get_sentiment(self):
        res = self.dashboard.get_sentiment()
        self.assertTrue(type(res)==Sentiment)

    def test_get_topic(self):
        res = self.dashboard.get_topic(1)
        self.assertTrue(len(res)>0)

    def test_get_topics(self):
        res = self.dashboard.get_topics('Suns')
        self.assertTrue(len(res)>0) # not collects data, so there are no topics

    def test_get_emotion_tweets(self):
        res = self.dashboard.get_emotion_tweets('Sad')
        self.assertTrue(len(res)>0) # not collects data, so there are no topics


    # # ----------------------------------- Users Options ------------------------------------------

    # def test_searchTweetsByKeywords(self):
    #     # user exists
    #     res = self.dashboard.searchTweetsByKeywords('username', 'Suns')
    #     self.assertEqual(True, res)
    #     # user isn't exist
    #     res = self.dashboard.searchTweetsByKeywords('user', 'Suns')
    #     self.assertEqual(False, res)

    def test_editTwittersTokens(self):
        # user is admin
        # tokens = {'token': 131312}
        tokens = [145454]
        res = self.dashboard.editTwittersTokens('username', tokens)
        self.assertEqual(True, res)
        # user isn't admin
        res = self.dashboard.editTwittersTokens('user', tokens)
        self.assertEqual(False, res)

    # # ----------------------------------- Manage Users --------------------------------------------

    def test_register(self):
        # already exists username
        res = self.dashboard.register('username', 'pass')
        self.assertEqual(False, res)
        # new username
        res = self.dashboard.register('user', '123')
        self.assertEqual(True, res)

    def test_login(self):
        # wrong password
        res = self.dashboard.login('username', 'pass')
        self.assertEqual(False, res)
        # not existing username
        res = self.dashboard.login('usernamelalala', 'pass')
        self.assertEqual(False, res)
        # correct details
        res = self.dashboard.login('username', '123')
        self.assertEqual(True, res)

    def test_deleteUser(self):
        # wrong password
        res = self.dashboard.deleteUser('username', 'pass')
        self.assertEqual(False, res)


if __name__ == '__main__':
    unittest.main()
