from sqlalchemy.exc import SQLAlchemyError

from PersistenceLayer.database import session

import threading
dblock = threading.Lock()
class BaseORM:
    def add_to_db(self):
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
