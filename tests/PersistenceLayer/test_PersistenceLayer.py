import unittest
from PersistenceLayer.database import session
# from PersistenceLayer.database import session
from PersistenceLayer.UsersORM import UserOrm

from .ExternalAPIsORM.test_ExtarnalAPIsORM import TestExternalAPIsORM
from .AnalysisORM.test_AnalysedTopics import TestAnalysedTopics
from .AnalysisORM.test_AnalysedTweets import TestAnalysedTweets
from .UsersORM.test_UsersORM import TestUsersORM


class TestPersistenceLayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        External = TestExternalAPIsORM()
        External.setUp()
        External.test_tables_connections()
        analysed = TestAnalysedTopics()
        analysed.setUp()
        analysed.topic.trend.append(External.trend)
        analysed.topic.topic_tweets = External.tweets
        analysed.test_add_topic()
        analysed = TestAnalysedTweets()

        analysed.setUp()
        analysed.tweet.tweet = External.tweets[0]
        analysed.test_add_tweet()
        user = TestUsersORM()
        user.setUp()
        user.test_add_user()
        External.search.user.append(user.user)
        External.search.update_db()

    def test_connection(self):
        user = session.query(UserOrm).filter_by(username="citrus").first()
        assert len(user.user_searches) > 0
        search = user.user_searches[0]
        assert len(search.tweets) == 2
        tweet = search.tweets[0]
        assert tweet.trend[0].content == "some"
        assert len(tweet.topics[0].tweets) == 2
        assert tweet.trend[0] == tweet.topics[0].trends[0]

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass


if __name__ == '__main__':
    unittest.main()
