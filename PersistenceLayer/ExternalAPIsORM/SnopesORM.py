from sqlalchemy.orm import relationship

from .ExternalAPITablesConnections import SnopesTweetsConnection
from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey


class SnopesORM(Base, BaseORM):
    __tablename__ = "snopes"
    claim_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    content = Column(String)
    Verdict = Column(String)
    Date = Column(String)
    snope_tweets = relationship('TweetORM', secondary=SnopesTweetsConnection, backref='snope')
    analyzed = relationship("AnalysedClaims", uselist=False, back_populates="claim")
