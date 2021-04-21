from sqlalchemy.exc import SQLAlchemyError

from PersistenceLayer.database import session
# import logging
import threading
dblock = threading.Lock()
# logging.basicConfig(filename='example.log', level=logging.DEBUG)
class BaseORM:
    def add_to_db(self):
        # logging.info('try add to db from '+str(type(self)))
        dblock.acquire()
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
        dblock.release()

    def update_db(self):
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
