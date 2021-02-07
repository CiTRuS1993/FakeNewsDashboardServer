from sqlalchemy.orm import relationship

from .ExternalAPITablesConnections import SearchTweetConnection
from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String,ForeignKey,ARRAY

from ..tablesConnections import SearchHistory


class SearchORM(Base,BaseORM):
    __tablename__ = "search"
    search_id = Column(Integer, primary_key=True, index=True)
    KeyWords = Column(String)
    user = relationship('UserOrm', secondary=SearchHistory, backref='searches')
    tweets = relationship('TweetORM', secondary=SearchTweetConnection, backref='search')
