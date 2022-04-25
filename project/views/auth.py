from flask import request
from flask_restx import Namespace, abort, Resource

from project.exceptions import ItemNotFound

from project.setup_db import db
from project.services.user_service import UserService
from project.tools.security import refresh_user_token, login_user

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Authorization Error")
    def post(self):
        """User's authorization """
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        try:
            user = UserService(db.session).get_item_by_email(email=req_json.get("email"))
            print(user)
            tokens = login_user(req_json, user)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")

    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    @auth_ns.response(401, "Authorization Error")
    def put(self):
        """Refresh token"""
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        try:
            tokens = refresh_user_token(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    @auth_ns.response(200, "Success")
    @auth_ns.response(400, "Bad Request")
    def post(self):
        """New user's registration"""
        req_json = request.json
        if not req_json:
            abort(400, message="Bad Request")
        return UserService(db.session).create(req_json), 200
