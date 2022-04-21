from sqlalchemy.orm import scoped_session

from project.dao.models.user import User


class AuthDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_username(self, data):
        return self._db_session.query(User).filter(User.username == data).first()
