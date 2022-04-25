from project.exceptions import ItemNotFound
from project.services import FavoriteMovieService
from project.setup_db import db
from project.tools.security import auth_required, auth_check
from flask_restx import Namespace, reqparse, Resource, abort

favorite_movie_ns = Namespace("favorites/movies")
parser = reqparse.RequestParser()
parser.add_argument('page', type=int)
parser.add_argument('status', type=str)


@favorite_movie_ns.route("/")
class FavoriteMoviesView(Resource):
    @favorite_movie_ns.response(200, "OK")
    @favorite_movie_ns.response(404, "Movie not found")
    @auth_required
    def get(self):
        """Get all favorite movies"""
        uid = auth_check().get("id")
        try:
            return FavoriteMovieService(db.session).get_by_user_id(uid)
        except ItemNotFound:
            abort(404, messages="Movie not Found")


@favorite_movie_ns.route("/<int:mid>")
class FavoriteMoviesView(Resource):

    @favorite_movie_ns.response(200, "OK")
    @favorite_movie_ns.response(404, "Movie not found")
    @auth_required
    def post(self, mid: int):
        """Add favorite movie"""
        uid = auth_check().get("id")
        return FavoriteMovieService(db.session).create(mid=mid, uid=uid)

    @favorite_movie_ns.response(200, "OK")
    @favorite_movie_ns.response(404, "Movie not found")
    @auth_required
    def delete(self, mid: int):
        """Delete favorite movie"""
        uid = auth_check().get("id")
        return FavoriteMovieService(db.session).delete(mid=mid, uid=uid)
