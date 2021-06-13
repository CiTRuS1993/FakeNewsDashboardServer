import unittest
from unittest import TestCase, mock

from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.manager = ExternalSystemsAPIsManagerInterface()

    def test_searchTweetsByKeywords(self):
        # return self.manager.searchTweetsByKeywords(keyword, token)        Yarin: probably bug
        pass

    def test_retrieveGoogleTrendsData(self):
        tweets = self.manager.retrieveGoogleTrendsData()
        self.assertTrue(len(tweets) > 0)

    def test_retrieveSnopesData(self):
        self.assertTrue(True)


    def test_editTwittersTokens(self, tokens):
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
