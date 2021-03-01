from .UserOrm import UserOrm
from ..ExternalAPIsORM.SearchORM import SearchORM
import jsonpickle
import json


class UsersORMFacade:
    def __init__(self):
        from ..database import session
        self.session = session
        self.add_user('username', '123', 'us@gmail.com', 'admin')

    def get_all_users(self):
        users = jsonpickle.dumps(self.session.query(UserOrm).all())
        jusers = json.loads(users)
        return jusers

    def get_user(self, username):
        user = jsonpickle.dumps(self.session.query(UserOrm).filter_by(username=username).first())
        juser = json.loads(user)
        return juser

    def add_user(self, username, password, email, role=None):
        UserOrm(username=username, password=password, email=email, role=role).add_to_db()

    def __setitem__(self, key, value):
        self.add_user(**value)

    def __getitem__(self, username):
        return self.get_user(username)

    def __delitem__(self, username):
        self.delete_user()

    def __iter__(self):
        for user in self.session.query(UserOrm):
            yield json.loads(jsonpickle.dumps(user))

    def delete_user(self, username=None):
        self.session.query(UserOrm).filter_by(username=username).first().delete_from_db()

    def add_search(self, username, search_id):
        user = self.session.query(UserOrm).filter_by(username=username).first()
        search = self.session.query(SearchORM).filter_by(search_id=search_id).first()
        user.search_history.append(search)
        user.update_db()

    def __len__(self):
        return self.session.query(UserOrm).count()
