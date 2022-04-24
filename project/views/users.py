from flask_restx import Namespace, Resource, reqparse, abort
from flask import request
from project.exceptions import ItemNotFound
from project.services.user_service import UserService
from project.setup_db import db
from project.tools.security import auth_required

users_ns = Namespace("users")
parser = reqparse.RequestParser()
parser.add_argument('page', type=int)


@users_ns.route("/")
class UsersView(Resource):
    @users_ns.expect(parser)
    @auth_required
    @users_ns.response(200, "OK")
    def get(self):
        page = parser.parse_args().get("page")
        if page:
            return UserService(db.session).get_limit_users(page)
        return UserService(db.session).get_all_users()


@users_ns.route("/<int:uid>")
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(400, "User not found")
    def get(self, uid: int):
        try:
            return UserService(db.session).get_item_by_id(uid)
        except ItemNotFound:
            abort(404, message="User not found")

    def patch(self, uid: int):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        if not req_json.get("id"):
            req_json['id'] = uid
        try:
            return UserService(db.session).update(req_json)
        except ItemNotFound:
            abort(404, message="User not found")

@users_ns.route("/password/<int:uid>")
class UserPatchView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def put(self, uid: int):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        if not req_json.get("password_1") or not req_json.get("password_2"):
            abort(400, message="Bad Request")
        if not req_json.get("id"):
            req_json['id'] = uid
        try:
            return UserService(db.session).update_pass(req_json)
        except ItemNotFound:
            abort(404, message="User not found")
