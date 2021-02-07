from sqlalchemy.exc import SQLAlchemyError

from PersistenceLayer.database import session


class BaseORM:
    def add_to_db(self):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()

    def update_db(self):
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()
