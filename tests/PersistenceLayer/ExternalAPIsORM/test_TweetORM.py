import os
from unittest import TestCase
from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL

from PersistenceLayer.ExternalAPIsORM.TweetORM import TweetORM


class TestTweetORM(TestCase):
    def setUp(self) -> None:
        self.tweet = TweetORM(id=str(0), author_name="@citrus", content="hello", date="02.02.21", retweet_count=0,
                              favorite_count=0)

    def test_add_tweet(self):
        assert session.query(TweetORM).filter_by(id=self.tweet.id).count() == 0

        self.tweet.add_to_db()
        assert session.query(TweetORM).filter_by(id=self.tweet.id).count() == 1

    def test_update_tweet(self):
        self.test_add_tweet()
        self.tweet.location = "somewhere over the rainbow"
        self.tweet.update_db()
        assert session.query(TweetORM).filter_by(id=self.tweet.id).first().location == "somewhere over the rainbow"

    def tearDown(self) -> None:
        if session.query(TweetORM).filter_by(id=self.tweet.id).count() == 1:
            session.delete(self.tweet)
            session.commit()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass

