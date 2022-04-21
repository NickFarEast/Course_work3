from .base import BaseMixin
from project.setup_db import db
from ...tools.security import get_hash_password


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    favorite_genre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User '{self.name.title()}'>"



    def compare_password(self, other_password) -> bool:
        hashed_password = get_hash_password(other_password)
        return hashed_password == self.password