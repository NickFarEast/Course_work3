from sqlalchemy.orm import scoped_session

from project.dao.models import FavoriteMovie


class FavoriteMovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_user_id(self, uid):
        return self._db_session.query(FavoriteMovie).filter(FavoriteMovie.user_id == uid).all()

    def create(self, uid, mid):
        obj = FavoriteMovie(user_id=uid, movie_id=mid)
        self._db_session.add(obj)
        self._db_session.commit()
        return obj

    def delete(self, uid, mid):
        obj = self._db_session.query(FavoriteMovie).filter(
            FavoriteMovie.user_id == uid,
            FavoriteMovie.movie_id == mid
        ).one_or_none()
        self._db_session.delete(obj)
        self._db_session.commit()
        return obj
