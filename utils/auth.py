import functools
import datetime
from calendar import timegm

from flask import request
import jwt

from utils.block import BLOCKLIST
from config import Config

key = Config.SECRET_KEY


def check_if_token_in_blocklist(jwt_payload):
    """Check if a user has already logged out or not

    If the user has already logged out, the token will be recorded in a block list.
    If a token in the block list has already expired, remove it.

    Parameters
    ----------
    jwt_payload: dictionary
        the body of the token that contains a unique field for that token

    Returns
    -------
    blocked: boolean
        whether a user has already logged out or not
    """

    blocked = False
    now = datetime.datetime.utcnow().utctimetuple()
    for token in BLOCKLIST:
        if token < timegm(now):
            BLOCKLIST.remove(token)
        if token == jwt_payload["exp"]:
            blocked = True
    return blocked


def jwt_required(f):
    """A decorator used to validate JWT

    Returns
    -------
    function
        the function that requires jwt
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Check if client has logged in or not
        if "Authorization" in request.headers:
            # First 7 character is the Authentication type
            token = request.headers["Authorization"][7:]
        else:
            return {"msg": "You need to log in first!"}, 401

        try:
            data = jwt.decode(token, key, algorithms="HS256")
            # Check if user has logged out or not
            if not check_if_token_in_blocklist(data):
                return f(*args, **kwargs, **data)
            return {"msg": "You has already logged out!"}, 401
        except jwt.exceptions.InvalidTokenError as e:
            return {"msg": str(e)}, 400
    return wrapper
