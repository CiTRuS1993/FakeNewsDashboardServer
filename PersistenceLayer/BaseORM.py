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
        dblock.acquire()
        try:
            session.commit()
        except:
            print("error in update_db")
        dblock.release()

    def delete_from_db(self):
        dblock.acquire()
        session.delete(self)
        session.commit()
        dblock.release()

    # def flush_db(self):
    #     # logging.info('try add to db from '+str(type(self)))
    #     dblock.acquire()
    #     try:
    #         # session.add(self)
    #         session.flush(self)
    #     except SQLAlchemyError as e:
    #         # dblock.release()
    #         session.rollback()
    #     dblock.release()