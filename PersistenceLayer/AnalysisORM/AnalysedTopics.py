from sqlalchemy.orm import relationship

from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String,ForeignKey

from ..tablesConnections import TopicsTrendsConnection, TopicsTweetsConnection


class AnalysedTopics(Base,BaseORM):
    __tablename__ = "analysed_topics"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    key_words = Column(String)
    prediction = Column(String)
    emotion = Column(String)
    sentiment = Column(Integer)
    topic_tweets = relationship('TweetORM', secondary=TopicsTweetsConnection, backref='tweet_topics')
    trend = relationship('TrendsORM', secondary=TopicsTrendsConnection, backref='topics')

