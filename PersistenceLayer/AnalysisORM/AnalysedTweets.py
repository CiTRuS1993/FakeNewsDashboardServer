from sqlalchemy.orm import relationship, backref

from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey


class AnalysedTweets(Base, BaseORM):
    __tablename__ = "analysed_tweets"
    id = Column(String, ForeignKey('tweets.id'), primary_key=True, index=True)
    prediction = Column(String)
    emotion = Column(String)
    sentiment = Column(Integer)
    tweet = relationship("TweetORM", uselist=False, back_populates="analyzed",
                         cascade="save-update, merge")
    # tweet = relationship("TweetORM", uselist=False, back_populates="analyzed")
