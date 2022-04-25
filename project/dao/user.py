from sqlalchemy.orm import scoped_session

from project.dao.models.user import User


class UserDAO():
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, uid):
        return self._db_session.query(User).filter(User.id == uid).one_or_none()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def get_limit(self, limit, offset):
        return self._db_session.query(User).limit(limit).offset(offset).all

    def create(self, data):
        user = User(**data)
        self._db_session.add(user)
        self._db_session.commit()
        return user

    def update(self, data):
        user = self.get_by_id(data.get('id'))
        if user:
            if data.get('password'):
                user.password = data.get('password')
            if data.get('role'):
                user.role = data.get('role')
            if data.get('name'):
                user.name= data.get('name')
            if data.get('surname'):
                user.surname = data.get('surname')
            if data.get('favorite_genre'):
                user.favorite_genre = data.get('favorite_genre')

        self._db_session.add(user)
        self._db_session.commit()
        return user


    def update_password(self, data):
        user = self.get_by_id(data.get('id'))
        if user:
            if data.get('password'):
                user.password = data.get('password')

        self._db_session.add(user)
        self._db_session.commit()
        return user