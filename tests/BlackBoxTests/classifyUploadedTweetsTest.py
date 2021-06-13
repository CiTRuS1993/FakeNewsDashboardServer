import unittest

from ServiceLayer.DashboardFacade import DashboardFacade

# test UC 6
class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dashboard = DashboardFacade('username', '123')
        self.file = 'tests\BlackBoxTests\export_posts_for_csv_importer.csv'
        self.wrong_file = 'tests\BlackBoxTests\export_posts_for_csv_importer.xls'

    def test_success(self):
        res= self.dashboard.classifyTweets('username', self.file)
        self.assertEqual(True, res)


    def test_fail(self):
        # no user
        res = self.dashboard.classifyTweets('user', self.file)
        self.assertEqual(False, res)
        # bad file format
        res = self.dashboard.classifyTweets('user', self.wrong_file)
        self.assertEqual(False, res)


if __name__ == '__main__':
    unittest.main()
