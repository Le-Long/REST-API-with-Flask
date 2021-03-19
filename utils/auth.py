import functools

from flask import jsonify, request
import jwt

from utils.block import BLOCKLIST

key = "4w5herd"


def check_if_token_in_blocklist(jwt_payload):
    """ """
    return str(jwt_payload["iat"]) in BLOCKLIST


def jwt_required(f):
    """ A decorator used for every methods that require JWT """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """ Check if client has logged in or not """
        if "Authorization" in request.headers:
            token = request.headers["Authorization"][7:]  # First 7 character is the Authentication type
        else:
            return jsonify({"msg": "Missing Authorization header!"})

        try:
            data = jwt.decode(token, key, algorithms="HS256")
            """ Check if user has logged out or not """
            if not check_if_token_in_blocklist(data):
                return f(*args, **kwargs, **data)
            return jsonify({"msg": "Token has been revoked!"})
        except jwt.exceptions.InvalidTokenError as e:
            return jsonify({"msg": str(e)})
    return wrapper
