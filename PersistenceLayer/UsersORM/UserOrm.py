from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship

from ..BaseORM import BaseORM
from ..database import Base, session
from sqlalchemy import Column, Integer, String

from ..tablesConnections import SearchHistory


class UserOrm(Base,BaseORM):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    role = Column(String)
    email = Column(String)
    user_searches = relationship('SearchORM', secondary=SearchHistory, backref='users')


