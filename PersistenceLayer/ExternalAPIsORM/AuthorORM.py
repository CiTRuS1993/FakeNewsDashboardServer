from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class AuthorORM(Base, BaseORM):
    __tablename__ = "authors"
    username = Column(String, primary_key=True, index=True)
    statuses_count = Column(Integer)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    listed_count = Column(Integer)
    tweets = relationship("TweetORM",backref="author")
