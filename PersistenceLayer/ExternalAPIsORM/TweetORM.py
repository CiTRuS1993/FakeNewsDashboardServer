from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from .ExternalAPITablesConnections import SnopesTweetsConnection
from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey,BigInteger

from ..tablesConnections import TopicsTweetsConnection


class TweetORM(Base,BaseORM):
    __tablename__ = "tweets"
    id = Column(String, primary_key=True, index=True)  # string?
    author_name = Column(String, ForeignKey('authors.username'))
    content = Column(String)
    location = Column(String)
    date = Column(String)

    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    snopes = relationship('SnopesORM', secondary=SnopesTweetsConnection, backref='tweets')
    topics = relationship('AnalysedTopics', secondary=TopicsTweetsConnection, backref='tweets')
    analyzed = relationship("AnalysedTweets", uselist=False, back_populates="tweet")

