import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def searchTweetsByKeywords(self, keyword, token):
        self.assertEqual(True, False)

    def retrieveGoogleTrendsData(self):
        self.assertEqual(True, False)

    def retrieveSnopesData(self):
        self.assertEqual(True, False)

    # tokens is list of strings
    def editTwittersTokens(self, tokens):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
