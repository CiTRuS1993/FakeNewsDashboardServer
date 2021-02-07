import sqlalchemy as db
from .database import Base,engine,session



Base.metadata.create_all(bind=engine)

