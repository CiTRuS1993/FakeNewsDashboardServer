import os
from unittest import TestCase
from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL

from PersistenceLayer.UsersORM.UserOrm import UserOrm


class TestUsersORM(TestCase):
    def setUp(self) -> None:
        self.user = UserOrm(username="citrus", password="pass", email="my@mail.co")

    def test_add_user(self):
        assert session.query(UserOrm).filter_by(username=self.user.username).count() == 0

        self.user.add_to_db()
        assert session.query(UserOrm).filter_by(username=self.user.username).count() == 1

    def test_update_tweet(self):
        self.test_add_user()
        self.user.email = "other@mail.co"
        self.user.update_db()
        assert session.query(UserOrm).filter_by(username=self.user.username).first().email == "other@mail.co"

    def tearDown(self) -> None:
        if session.query(UserOrm).filter_by(username=self.user.username).count() == 1:
            session.delete(self.user)
            session.commit()

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass
