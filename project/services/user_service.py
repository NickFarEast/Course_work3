from flask import current_app
from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import get_hash_password


class UserService(BaseService):
    def get_item_by_id(self, uid):
        user = UserDAO(self._db_session).get_by_id(uid)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_limit_users(self,page):
        limit = current_app.config["ITEMS_PER_PAGE"]
        offset = (page - 1) * limit
        users = UserDAO(self._db_session).get_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, data):
        user_pass = data.get("password")
        if user_pass:
            data["password"] = get_hash_password(user_pass)
        user = UserDAO(self._db_session).create(data)
        return UserSchema().dump(user)

    def update(self, data):
        user = UserDAO(self._db_session).update(data)
        return UserSchema().dump(user)

    def update_pass(self, data):
        user_pass_1 = data.get("password_1")
        user_pass_2 = data.get("password_2")
        if user_pass_1 != user_pass_2:
            data["password"] = get_hash_password(user_pass_2)
        user = UserDAO(self._db_session).update_password(data)
        return UserSchema().dump(user)
