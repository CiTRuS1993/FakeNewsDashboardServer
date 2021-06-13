import unittest
from unittest import TestCase, mock

from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.manager = ExternalSystemsAPIsManagerInterface()


    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.TwitterManager")
    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.GoogleTrendsManager")
    def retrieveGoogleTrendsData(self, google_mock, twitter_mock):
        self.manager.extrenalManagerLogic.twitterManager = twitter_mock
        self.manager.extrenalManagerLogic.googleTrendsManager = google_mock

        tweets = self.manager.retrieveGoogleTrendsData()
        self.assertTrue(len(tweets) > 0)
        return

    def retrieveSnopesData(self):
        pass


    def editTwittersTokens(self, tokens):
        pass


    # def test_searchTweetsByKeywords(self):
    #     # return self.manager.searchTweetsByKeywords(keyword, token)        Yarin: probably bug
    #     pass

if __name__ == '__main__':
    unittest.main()
