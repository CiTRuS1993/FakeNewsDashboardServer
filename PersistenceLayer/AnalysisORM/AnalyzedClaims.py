from sqlalchemy.orm import relationship

from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String, ForeignKey

from ..tablesConnections import TopicsTrendsConnection, TopicsTweetsConnection


class AnalysedClaims(Base, BaseORM):
    __tablename__ = "analysed_claims"
    id = Column(String, ForeignKey('snopes.claim_id'), primary_key=True, index=True)
    prediction = Column(String)
    emotion = Column(String)
    sentiment = Column(Integer)
    claim = relationship("SnopesORM", uselist=False, back_populates="analyzed")

