from unittest import TestCase
from PersistenceLayer.UsersORM.UsersORMFacade import UsersORMFacade
from .test_UsersORM import TestUsersORM
import json

class TestUsersORMFacade(TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        adduser = TestUsersORM()
        adduser.setUp()
        adduser.test_add_user()


    def setUp(self) -> None:
        self.facade = UsersORMFacade()

    def test_get_all_users(self):
        users = self.facade.get_all_users()
        assert len(users) == 1
        self.facade['citrus']
    def test_get_user(self):
        self.fail()
