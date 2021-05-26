import time
from unittest import TestCase

from BuisnessLayer.ExternalSystemsAPIsManager.ExternalSystemsFacade import ExternalSystemsFacade


class TestExternalSystemsFacade(TestCase):
    def setUp(self) -> None:
        self.api = ExternalSystemsFacade()

    def test_search_tweets_by_keywords(self):
        tweets = self.api.search_tweets_by_keywords(0,'key')
        assert tweets


    def test_retrieve_google_trends_data(self):
        time.sleep(120)
        tweets = self.api.retrieve_google_trends_data()
        assert tweets


