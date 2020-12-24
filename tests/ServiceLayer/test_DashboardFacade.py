import time
import unittest

from ServiceLayer.DashboardFacade import DashboardFacade


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.dashboard = DashboardFacade("hadar","pass")
    # ------------------------------- Retrieve Data & External Systems -----------------------------

    # gets all data related to the dashboard
    def test_retrieveFakeNewsData(self):
        self.assertEqual(True, False)

    # gets all data related to the Google Trends window
    def test_googleTrendsStatistics(self):
        self.assertEqual(True, False)

    # gets all data related to the Snopes window
    def test_snopesStatistics(self):
        self.assertEqual(True, False)

    # each 12 hours retrieve the new Google Trends topics
    def test_retrieveGoogleTrendsData(self):
        time.sleep(4)
        self.dashboard.retrieveGoogleTrendsData()
        time.sleep(4)
        print(self.dashboard.retrieveFakeNewsData())

    # each 12 hours retrieve the new Snopes claims
    def test_retrieveSnopesData(self):
        self.assertEqual(True, False)

    def test_configClassifier(self):
        self.assertEqual(True, False)

    # ----------------------------------- Users Options ------------------------------------------

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

    def test_register(self):
        self.assertEqual(True, False)

    def test_login(self):
        self.assertEqual(True, False)

    def test_deleteUser(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
