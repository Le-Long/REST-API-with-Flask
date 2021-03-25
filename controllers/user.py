import datetime

from flask import request, Blueprint
import jwt

from schema.user import ValidateUserInputSchema
from utils.log import log_and_capture
from utils.block import BLOCKLIST
from utils.auth import key, jwt_required
from models.user import UserModel

user_page = Blueprint("user_page", __name__)


def validate_user_input():
    """Validate user's information on the request body"""
    auth_schema = ValidateUserInputSchema()
    data = auth_schema.load(request.json)
    return data


@user_page.route("/register", methods=["POST"], endpoint="sign_up")
@log_and_capture(endpoint="sign_up")
def post():
    """Handle the request of signing up

    Return:
    Message: dictionary
        format {"msg": The message}
    Status code: int
        400 if the request is not valid
        201 if OK
    """

    # Validate information of the new user
    data = validate_user_input()
    if UserModel.find_by_username(data["username"]):
        return {"msg": "An user with that username already exists"}, 200

    # Create a new user
    user = UserModel(**data)
    user.save_to_db()

    return {"msg": "User created successfully."}, 201


@user_page.route("/login", methods=["POST"], endpoint="sign_in")
@log_and_capture(endpoint="sign_in")
def post():
    """Handle the request of signing in

    Return:
    Access token if success: dictionary
        format {"access_token": The token}
    Message if error: dictionary
        format {"msg": The error message}
    Status code: int
        401 if the request is unauthorized
        200 if OK
    """

    data = validate_user_input()

    # Return an access token with the user id and
    # the time the token was created so that we can distinguish them
    user = UserModel.find_by_username(data["username"])
    if user and user.verify_password(data["password"]):
        now = datetime.datetime.utcnow()
        access_token = jwt.encode({"identity": user.id,
                                   "exp": now + datetime.timedelta(minutes=30)},
                                  key, algorithm="HS256")
        return {"access_token": access_token}, 200
    return {"msg": "Please register first!"}, 401


@user_page.route("/logout", methods=["POST"], endpoint="sign_out")
@log_and_capture(endpoint="sign_out")
@jwt_required
def post(**token):
    """Handle the request of signing up

    Arguments:
    Token: dictionary
        format {"identity": user id, "iat": the time the token was created}

    Return:
    Message: dictionary
        format {"msg": The message}
    Status code: int
        200 if OK
    """

    # Handle the request of signing out by adding the present token to block list
    BLOCKLIST.add(token["exp"])
    return {"msg": "Successfully logged out!"}, 200
