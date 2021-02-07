from sqlalchemy.orm import relationship

from .ExternalAPITablesConnections import TrendsTweetsConnection
from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String,ForeignKey

from ..tablesConnections import TopicsTrendsConnection


class TrendsORM(Base,BaseORM):
    __tablename__ = "trends"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    date = Column(String)
    tweets = relationship('TweetORM', secondary=TrendsTweetsConnection, backref='trend')
    trend_topics = relationship('AnalysedTopics', secondary=TopicsTrendsConnection, backref='trends')


