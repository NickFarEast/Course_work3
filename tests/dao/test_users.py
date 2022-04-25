import pytest

from project.dao.user import UserDAO
from project.dao.models.user import User


class TestUserDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(email='test', password="test", name="test", surname="test", favorite_genre="test", role="test")
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(email='test2', password="test2", name="test2", surname="test2", favorite_genre="test2", role="test2")
        db.session.add(u)
        db.session.commit()
        return u



    def test_get_user_by_id(self, user_1):
        assert self.dao.get_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None

    def test_get_all_users(self, user_1, user_2):
        assert self.dao.get_all() == [user_1, user_2]