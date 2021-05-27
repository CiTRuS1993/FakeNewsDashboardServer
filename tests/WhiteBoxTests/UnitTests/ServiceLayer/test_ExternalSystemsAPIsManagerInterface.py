import time
from unittest import TestCase

from ServiceLayer.ExternalSystemsAPIsManagerInterface import ExternalSystemsAPIsManagerInterface


class TestExternalSystemsAPIsManagerInterface(TestCase):
    def setUp(self) -> None:
        self.externalSystemsAPI = ExternalSystemsAPIsManagerInterface()
    def test_search_tweets_by_keywords(self):
        self.assertEqual(True, False)

    def test_retrieve_google_trends_data(self):
        time.sleep(15)
        print(self.externalSystemsAPI.retrieveGoogleTrendsData())

        self.externalSystemsAPI.extrenalManagerLogic.twitterManager.stop()

    def test_retrieve_snopes_data(self):
        self.assertEqual(True, False)

    def test_edit_twitters_tokens(self):
        self.assertEqual(True, False)
