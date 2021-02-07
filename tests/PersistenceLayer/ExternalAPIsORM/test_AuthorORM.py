import os
from unittest import TestCase

from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL
from PersistenceLayer.ExternalAPIsORM import AuthorORM, TweetORM


class TestAuthorORM(TestCase):
    def setUp(self) -> None:
        self.author = AuthorORM(username="@citrus", statuses_count=0, followers_count=0, friends_count=0,
                                listed_count=0)

    def test_add_tweet(self):
        assert session.query(AuthorORM).filter_by(username=self.author.username).count() == 0

        self.author.add_to_db()
        assert session.query(AuthorORM).filter_by(username=self.author.username).count() == 1

    def test_update_tweet(self):
        self.test_add_tweet()
        self.author.followers_count = 1
        self.author.update_db()
        assert session.query(AuthorORM).filter_by(username=self.author.username).first().followers_count == 1

    def tearDown(self) -> None:
        if session.query(AuthorORM).filter_by(username=self.author.username).count() == 1:
            session.delete(self.author)
            session.commit()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass
