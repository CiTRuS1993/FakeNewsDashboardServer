import unittest

from ServiceLayer.DashboardFacade import DashboardFacade


# test UC 1
class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.admin_name = "username"
        self.admin_pass = "123"

    def test_success(self):
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        self.assertEqual(True, len(dashboard.analysisManager.getGoogleTrendsStatistics()) > 0)
        self.assertEqual(True, dashboard.usersManager.is_admin(self.admin_name))
        self.assertEqual(True, dashboard.externalSystemsManager.extrenalManagerLogic.twitterManager.is_connected())

    def test_fail(self):
        # wrong username
        with self.assertRaises(SystemExit) as cm:
            DashboardFacade(self.admin_name + 'lalala', self.admin_pass)
            self.assertEqual(cm.exception, "Wrong username or password!")
        # wrong password
        with self.assertRaises(SystemExit) as cm:
            DashboardFacade(self.admin_name, self.admin_pass+ 'lalala')
            self.assertEqual(cm.exception, "Wrong username or password!")
        # connection problems
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        dashboard.externalSystemsManager.extrenalManagerLogic.twitterManager.api = None
        dashboard.externalSystemsManager.extrenalManagerLogic.googleTrendsManager.pytrends = None
        dashboard.analysisManager.analysisManagerLogic.trends_statistics = {}  # clear the DBs data
        with self.assertRaises(Exception) as cm:
            dashboard.retrieveGoogleTrendsData()
            self.assertEqual(cm.exception, "Connection problems")


if __name__ == '__main__':
    unittest.main()