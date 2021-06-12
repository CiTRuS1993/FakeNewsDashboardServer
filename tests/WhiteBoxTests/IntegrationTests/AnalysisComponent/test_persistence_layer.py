import random
import unittest
from datetime import datetime

from faker import Faker

from PersistenceLayer.AnalysisORM.AnalysisORMFacade import AnalysisORMFacade
from PersistenceLayer.ExternalAPIsORM.ExternalAPIsORMFacade import ExternalAPIsORMFacade


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.orm = AnalysisORMFacade()
        self.tweet_id = random.randint(1, 9999999)
        self.trend_id = 8
        self.fake = Faker()
        self.keywords = self.fake.text()
        date = datetime.today().date()
        external_orm = ExternalAPIsORMFacade()
        self.trend_id = external_orm.add_trend("test content", date)
        external_orm.add_tweet(self.tweet_id, "name", self.keywords, self.fake.address(),
                               date, is_test=True)


#   ----------------------- Tweets -----------------------

    def test_add_analyzed_tweet(self):
        self.assertTrue(self.orm.add_analyzed_tweet(self.tweet_id, "true", "happy", 2))
        self.assertFalse(self.orm.add_analyzed_tweet(self.tweet_id, "true", "happy", 2))

    def test_get_all_analyzed_tweets(self):
        tweets = self.orm.get_all_analyzed_tweets()
        self.assertTrue(len(tweets) > 0)

    def test_get_analyzed_tweet(self):
        self.orm.add_analyzed_tweet(self.tweet_id, "fake", "happy", 2)
        tweet = self.orm.get_analyzed_tweet(self.tweet_id)
        self.assertTrue(tweet is not None)

#   ----------------------- Topics -----------------------

    def test_add_analyzed_topic(self):
        topic_id = self.orm.add_analyzed_topic(self.keywords, "true", "sad", -1, [self.tweet_id], self.trend_id)
        self.assertTrue(topic_id > 0)
        self.assertFalse(self.orm.add_analyzed_topic(self.keywords, "true", "sad", -1,
                                                     [self.tweet_id], self.trend_id))

    def test_get_all_analyzed_topics(self):
        topics = self.orm.get_all_analyzed_topics()
        self.assertTrue(len(topics) > 0)

    def test_get_analyzed_topic(self):
        topic_id = self.orm.add_analyzed_topic(self.keywords, "true", "sad", -1, [self.tweet_id], self.trend_id)
        topic = self.orm.get_analyzed_topic(self.keywords)
        self.assertTrue(topic is not None)

    def test_get_all_trends(self):
        trends = self.orm.get_all_trends()
        self.assertTrue(len(trends) > 0)


#   ----------------------- Claims -----------------------

    def test_add_analyzed_claim(self):
        self.assertTrue(True)

    def test_get_all_analyzed_claims(self):
        self.assertTrue(True)

    def test_get_analyzed_claim(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
