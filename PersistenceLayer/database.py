from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "./test.db"

engine = create_engine(
    "sqlite:///"+SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# engine = create_engine("sqlite:///"+SQLALCHEMY_DATABASE_URL) # TODO?
# Session = sessionmaker(autocommit=True, autoflush=False, bind=engine)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
Base = declarative_base()
import PersistenceLayer.UsersORM
import PersistenceLayer.ExternalAPIsORM
import PersistenceLayer.AnalysisORM