import os
from unittest import TestCase

import PersistenceLayer
from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL

from PersistenceLayer.AnalysisORM import AnalysedTweets


class TestAnalysedTweets(TestCase):
    def setUp(self) -> None:
        self.tweet = AnalysedTweets(id=str(10765432100123456789), prediction="Fake", emotion="happy", sentiment=1)

    def test_add_tweet(self):
        assert session.query(AnalysedTweets).filter_by(id=self.tweet.id).count() == 0

        self.tweet.add_to_db()
        assert session.query(AnalysedTweets).filter_by(id=self.tweet.id).count() == 1

    def test_update_tweet(self):
        self.test_add_tweet()
        self.tweet.prediction = "True"
        self.tweet.update_db()
        assert session.query(AnalysedTweets).filter_by(id=self.tweet.id).first().prediction == "True"

    def tearDown(self) -> None:
        if session.query(AnalysedTweets).filter_by(id=self.tweet.id).count() == 1:
            session.delete(self.tweet)
            session.commit()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass
