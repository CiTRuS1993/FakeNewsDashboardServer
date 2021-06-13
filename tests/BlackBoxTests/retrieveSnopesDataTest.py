import unittest

from ServiceLayer.DashboardFacade import DashboardFacade

# test UC 5

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.admin_name = "username"
        self.admin_pass = "123"

    def test_success(self):
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) > 0)
        # no statistics
        dashboard.analysisManager.analysisManagerLogic.snopes_statistics = {}
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) == 0)

    def test_fail(self):
        # no data
        dashboard = DashboardFacade(self.admin_name, self.admin_pass)
        dashboard.externalSystemsManager.extrenalManagerLogic.twitterManager.api = None
        dashboard.externalSystemsManager.extrenalManagerLogic.snopesManager.snopes= {}
        self.assertEqual(True, len(dashboard.analysisManager.getSnopesStatistics()) == 0)


if __name__ == '__main__':
    unittest.main()
