from unittest import TestCase, mock
from BuisnessLayer.Users.UsersManagerFacade import UserManagerFacade
from tests.buisnessLayer.AnalysisManager.TestsObjects import userObject



class testUserManager(TestCase):
    def setUp(self) -> None:
        self.UserManagerFacade = UserManagerFacade("username", "123")


    @mock.patch("PersistenceLayer.UsersORM.UsersORMFacade")
    def test_init_userDb(self,mock):
        self.UserManagerFacade.users_db = mock
        mock.get_all_users.return_value = []
        self.assertEqual(self.UserManagerFacade.initUsersDB(), {})
        user1 = userObject('Guest',1,'Yarin','123')  # 'Yarin'
        user2 = userObject('Guest',2,'Sapir','123')  # 'Sapir'
        mock.get_all_users.return_value = [user1, user2] # User(...)
        self.assertEqual(self.UserManagerFacade.initUsersDB(), {'Yarin':user1, 'Sapir': user2}) #'username':User



    def test_register(self):
        self.assertFalse(self.UserManagerFacade.register("sapir", "sap3232"))
        self.assertTrue(self.UserManagerFacade.register("yarin", "sap3232"))
        self.assertTrue(self.UserManagerFacade.validate_user("sapir", "sap3232"))
        self.assertTrue(self.UserManagerFacade.validate_user("yarin", "sap3232"))
        self.assertFalse(self.UserManagerFacade.validate_user("sapir", "hadar12"))

    def test_admin_exists(self):
        self.assertFalse(self.UserManagerFacade.admin_exists("yarin", "sap3232"))
        self.assertTrue(self.UserManagerFacade.admin_exists("sapir", "sap3232"))

    def test_save_search_tweets_by_keywords(self):
        self.assertTrue(self.UserManagerFacade.save_search_tweets_by_keywords("sapir",1))

    def test_tag_tweet(self):
        self.assertTrue(self.UserManagerFacade.tag_tweet("sapir", 2))

    def test_view_user_search_history(self):
        self.assertFalse(self.UserManagerFacade.view_user_search_history("sa"))
        self.assertEqual([], self.UserManagerFacade.view_user_search_history("sapir"))

    def test_login(self):
        self.assertTrue(self.UserManagerFacade.login("sapir","sap3232"))

    def test_delete_user(self):
        self.assertTrue(self.UserManagerFacade.delete_user("sapir"))

    def test_is_admin(self):
        self.assertTrue(self.UserManagerFacade.is_admin("sapir"))

    def test_validate_user(self):
        self.assertTrue(self.UserManagerFacade.validate_user("sapir", "sap3232"))

    def test_classify_tweets(self):
        self.assertTrue(self.UserManagerFacade.classify_tweets("sapir",1))
        self.assertFalse(self.UserManagerFacade.classify_tweets("hadar", 1))

    def test_user_exists(self):
        self.assertTrue(self.UserManagerFacade.user_exists("sapir"))