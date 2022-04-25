from project.dao.favorite_movie import FavoriteMovieDAO
from project.exceptions import ItemNotFound
from project.schemas.favorite_movie import FavoriteMovieSchema
from project.services.base import BaseService


class FavoriteMovieService(BaseService):
    def get_by_user_id(self, uid):
        movies = FavoriteMovieDAO(self._db_session).get_by_user_id(uid)
        if not movies:
            raise ItemNotFound
        return FavoriteMovieSchema(many=True).dump(movies)

    def create(self, uid, mid):
        movie = FavoriteMovieDAO(self._db_session).create(uid, mid)
        return FavoriteMovieSchema().dump(movie)

    def delete(self, uid, mid):
        movie = FavoriteMovieDAO(self._db_session).delete(uid, mid)
        return FavoriteMovieSchema().dump(movie)
