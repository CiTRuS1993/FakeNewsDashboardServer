import unittest
from datetime import datetime
import random
from unittest import mock

from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade
from faker import Faker

class TestExternalSystems_PersistenceLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.orm = ExternalAPIsORMFacade()
        self.fake = Faker()
        self.trend_id = 8
        self.date = datetime.today().date()
        self.tweet1_id = random.randint(1, 9999999)
        self.tweet2_id = random.randint(1, 9999999)



 # ---------------------- ORMF & GoogleTrends --------------------------------------

    def test_add_trend(self):
        self.trend_id = self.orm.add_trend(self.fake.text(), self.date)
        self.assertTrue(self.trend_id > 0)

    def test_get_all_trends(self):
        trends = self.orm.get_all_trends()
        self.assertTrue(len(trends) > 0)
        for trend_keywords in trends.keys():
            for trend_i in trends[trend_keywords]:
                self.assertTrue('date' in trend_i.keys())
                self.assertTrue('id' in trend_i.keys())
                self.assertTrue(trend_i['id'] > 0)

    def test_get_trends_names_from_date(self):
        trends = self.orm.get_trends_names_from_date(self.date)
        self.assertTrue(len(trends) > 0)

    def test_get_trend(self):
        if self.trend_id > -1:
            trend = self.orm.get_trend(self.trend_id)
            self.assertTrue(len(trend) > 0)

# --------------------------- ORMF & Twitter --------------------------------

    @mock.patch("PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade")
    def test_add_tweet(self, mock):
        self.orm.add_tweet_to_author = mock
        name = self.fake.name()
        content = self.fake.text()
        location = self.fake.address()
        self.assertTrue(self.orm.add_tweet(self.tweet1_id, name, content, location,
                                           self.date, is_test=True))
        self.assertFalse(self.orm.add_tweet(self.tweet1_id, name, content, location,
                                            self.date, is_test=True))

        # trend_id= self.orm.add_trend(self.fake.text(), self.date)
        self.assertTrue(self.orm.add_tweet(self.tweet2_id, name, content, location,
                                           self.date, self.trend_id, is_test=True))
        self.assertFalse(self.orm.add_tweet(self.tweet2_id, name, content, location,
                                            self.date, self.trend_id, is_test=True))

    def test_get_all_tweets_dict(self):
        tweets = self.orm.get_all_tweets_dict()
        self.assertTrue(len(tweets) > 0)

    def test_get_tweet(self):
        self.orm.add_tweet(self.tweet1_id, self.fake.name(), self.fake.text(), self.fake.address(), self.date)
        tweet1 = self.orm.get_tweet(self.tweet1_id)
        self.assertTrue(tweet1 is not None)
        # tweet2 = self.orm.get_tweet(self.tweet2_id)
        # self.assertTrue(tweet2 is not None)

# ------------------------- ORMF & Snopes -------------------------------

    # TODO
    def test_add_snopes(self):
        pass

# --------------------------- others ----------------------------------------

    # TODO
    def test_add_search(self):
        pass

    # TODO
    def test_add_author(self):
        pass

    # TODO
    def test_add_tweet_to_author(self):
        pass

if __name__ == '__main__':
    unittest.main()
