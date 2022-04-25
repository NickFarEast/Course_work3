import base64
import hashlib

import jwt
from flask import current_app, request, abort
from datetime import datetime, timedelta
from typing import Dict

from project.exceptions import ItemNotFound


def get_hash_password(password: str) -> str:
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )).decode('utf-8')


def generate_tokens(data: dict) -> Dict[str, str]:
    data['exp'] = datetime.utcnow() + timedelta(minutes=30)
    data['refresh_token'] = False

    access_token: str = jwt.encode(
        payload=data,
        key=current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )

    data['exp'] = datetime.utcnow() + timedelta(days=30)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_from_headers(headers: dict):
    if 'Authorization' not in request.headers:
        abort(401)

    return headers['Authorization'].split('Bearer ')[-1]


def decode_token(token: str, refresh_token=False):
    decoded_token = {}

    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=current_app.config["SECRET_KEY"],
            algorithms=current_app.config["JWT_ALGORITHM"])
    except jwt.PyJWTError:
        current_app.logger.info('Got wrong token:"%s"', token)
        abort(401)

    if decoded_token['refresh_token'] != refresh_token:
        abort(400, 'Got wrong token type.')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_headers(request.headers)
        decode_token(token)

        return func(*args, **kwargs)

    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_headers(request.headers)
        decoded_token = decode_token(token)
        if decoded_token.get('role') != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def compare_password(other_password, password_hash):
    hashed_password = get_hash_password(other_password)
    return hashed_password == password_hash


def login_user(req_json, user):
    user_email = req_json.get("email")
    user_pass = req_json.get("password")
    if user_email and user_pass:
        pass_hashed = user["password"]
        req_json["role"] = user["role"]
        req_json["id"] = user["id"]
        if compare_password(password_hash=pass_hashed, other_password=user_pass):
            return generate_tokens(req_json)
    raise ItemNotFound


def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = decode_token(refresh_token)
    if data:
        tokens = generate_tokens(data)
        return tokens
    raise ItemNotFound

def auth_check():
    token = get_token_from_headers(request.headers)
    return decode_token(token)

