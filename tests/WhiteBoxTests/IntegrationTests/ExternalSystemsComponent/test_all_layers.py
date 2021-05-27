import unittest
from unittest import TestCase, mock

from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.manager = ExternalSystemsAPIsManagerInterface()

    def test_searchTweetsByKeywords(self):
        # return self.manager.searchTweetsByKeywords(keyword, token)        Yarin: probably bug TODO?
        pass

    def retrieveGoogleTrendsData(self):
        tweets = self.manager.retrieveGoogleTrendsData()
        self.assertTrue(len(tweets) > 0)
        return

    def retrieveSnopesData(self):
        # TODO
        pass


    def editTwittersTokens(self, tokens):
        # TODO- its written with bugs
        pass



if __name__ == '__main__':
    unittest.main()
