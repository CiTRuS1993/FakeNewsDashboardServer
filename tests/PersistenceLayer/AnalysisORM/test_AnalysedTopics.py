import os
from unittest import TestCase
from PersistenceLayer.database import session, SQLALCHEMY_DATABASE_URL

from PersistenceLayer.AnalysisORM import AnalysedTopics


class TestAnalysedTopics(TestCase):
    def setUp(self) -> None:
        self.topic = AnalysedTopics(id=0, key_words="key, words", prediction="Fake", emotion="happy", sentiment=1)

    def test_add_topic(self):
        assert session.query(AnalysedTopics).filter_by(id=self.topic.id).count() == 0

        self.topic.add_to_db()
        assert session.query(AnalysedTopics).filter_by(id=self.topic.id).count() == 1

    def test_update_tweet(self):
        self.test_add_topic()
        self.topic.prediction = "True"
        self.topic.update_db()
        assert session.query(AnalysedTopics).filter_by(id=self.topic.id).first().prediction == "True"

    def tearDown(self) -> None:
        if session.query(AnalysedTopics).filter_by(id=self.topic.id).count() == 1:
            session.delete(self.topic)
            session.commit()
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     if os.path.exists(SQLALCHEMY_DATABASE_URL):
    #         print("cleaning file")
    #         os.remove(SQLALCHEMY_DATABASE_URL)
    #     pass
