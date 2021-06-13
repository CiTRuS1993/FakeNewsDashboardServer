import unittest

from ServiceLayer.DashboardFacade import DashboardFacade

# test UC 3

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.admin_name = "username"
        self.admin_pass = "123"

    def test_success(self):
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        self.assertEqual(True, len(dashboard.analysisManager.getGoogleTrendsStatistics()) > 0)
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) > 0)
        # no statistics
        dashboard.analysisManager.analysisManagerLogic.trends_statistics = {}
        self.assertEqual(True, len(dashboard.analysisManager.getGoogleTrendsStatistics()) == 0)
        dashboard.analysisManager.analysisManagerLogic.snopes_statistics = {}
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) == 0)

    def test_fail(self):
        # connection problems
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        dashboard.externalSystemsManager.extrenalManagerLogic.twitterManager.api = None
        dashboard.externalSystemsManager.extrenalManagerLogic.googleTrendsManager.pytrends=None
        dashboard.analysisManager.analysisManagerLogic.trends_statistics={} # clear the DBs data
        with self.assertRaises(Exception) as cm:
            dashboard.retrieveGoogleTrendsData()
            self.assertEqual(cm.exception, "Connection problems")
        self.assertEqual(True, len(dashboard.analysisManager.getGoogleTrendsStatistics()) == 0)
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) == 0)


if __name__ == '__main__':
    unittest.main()
