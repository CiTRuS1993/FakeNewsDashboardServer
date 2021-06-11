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

    def test_fail(self):
        # wrong username
        dashboard = DashboardFacade(self.admin_name + 'lalala', self.admin_pass)
        self.assertEqual(False, len(dashboard.analysisManager.getGoogleTrendsStatistics()) > 0)
        self.assertEqual(False, dashboard.usersManager.is_admin(self.admin_name + 'lalala'))


if __name__ == '__main__':
    unittest.main()


    # @logger
    def test_success(self):
        # all valid details
        res = self.appoint_additional_manager(self.__appointee_name, self._store_name, [])
        self.assertTrue(res)


    # @logger
    def test_fail(self):
        # store doesn't exist
        res = self.appoint_additional_manager(self.__appointee_name, "someStoreName", [])
        self.assertFalse(res['response'])
        # user doesn't exist
        res = self.appoint_additional_manager("someUser", self._store_name, [])
        self.assertFalse(res['response'])
        # user isn't registered
        self.delete_user(self.__appointee_name)
        res = self.appoint_additional_manager(self.__appointee_name, self._store_name, [])
        self.assertFalse(res['response'])


    # @logger
    def tearDown(self) -> None:
        self.remove_store(self._store_name)
        self.delete_user(self._username)
        self.delete_user(self.__appointee_name)
