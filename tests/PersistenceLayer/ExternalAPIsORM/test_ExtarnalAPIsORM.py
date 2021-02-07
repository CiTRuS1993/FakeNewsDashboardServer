import os
import unittest
from PersistenceLayer.ExternalAPIsORM import *
from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL


class TestExternalAPIsORM(unittest.TestCase):
    def setUp(self) -> None:
        tweets = [TweetORM(id=str(10765432100123456789), author_name="@citrus", content="some", location="somewhere",
                           date="4.2.21",
                           retweet_count=0, favorite_count=0),
                  TweetORM(id=str(10765432100123456790), author_name="@citrus", content="something_else",
                           location="somewhere",
                           date="4.2.21", retweet_count=0, favorite_count=0)]
        self.tweets = tweets
        self.author = AuthorORM(username="@citrus", statuses_count=2, followers_count=0, friends_count=0,
                                listed_count=0, tweets=tweets)
        self.search = SearchORM(search_id=0, KeyWords="some,some", tweets=tweets)
        self.trend = TrendsORM(id=0, content="some", date="4.2.21", tweets=tweets)

    def test_tables_connections(self):
        for tweet in self.tweets:
            tweet.add_to_db()
        self.author.add_to_db()
        self.search.add_to_db()
        self.trend.add_to_db()
        assert session.query(TrendsORM).count() == 1
        assert len(session.query(TrendsORM).first().tweets) == 2
        tweet = session.query(TrendsORM).first().tweets[0]
        assert tweet.author.username == "@citrus"
        assert tweet.search[0].search_id == 0

    def tearDown(self) -> None:
        for tweet in self.tweets:
            tweet.delete_from_db()
        self.author.delete_from_db()
        self.search.delete_from_db()
        self.trend.delete_from_db()
        assert session.query(TweetORM).count() == 0
        assert session.query(AuthorORM).count() == 0
        assert session.query(TrendsORM).count() == 0
        assert session.query(SearchORM).count() == 0

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass
