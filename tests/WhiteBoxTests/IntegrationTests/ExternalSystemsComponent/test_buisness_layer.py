import time
import unittest
from unittest import TestCase, mock
import random

from BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade import ExternalSystemsFacade


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.facade = ExternalSystemsFacade()

    def test_search_tweets_by_keywords(self):
    #     self.facade.search_tweets_by_keywords(search_id, keyword)     TODO?
        pass

    @mock.patch("BuisnessLayer.ExternalSystemsAPIsManager.TwitterManager")
    @mock.patch("PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade")
    def test_retrieve_google_trends_data(self, orm_mock, twitter_mock):
        self.facade.googleTrendsManager.ExternalOrm = orm_mock
        self.facade.twitterManager.orm = orm_mock
        # tweets = {}   TODO
        self.facade.twitterManager = twitter_mock
        # twitter_mock.search_tweets_by_keywords.return_value = tweets  TODO
        tweets1 = self.facade.retrieve_google_trends_data()
        time.sleep(10)
        tweets2 = self.facade.retrieve_google_trends_data()
        self.assertTrue(len(tweets1) + len(tweets2) > 0)

    def test_edit_twitters_tokens(self):
        token1 = random.randint(1000000, 9999999999)
        token2 = random.randint(1000000, 9999999999)
        self.assertTrue(self.facade.edit_twitters_tokens([token1, token2]))

    def test_retrieve_snopes_data(self):
        # TODO
        pass
        # return self.facade.retrieve_snopes_data()


if __name__ == '__main__':
    unittest.main()
