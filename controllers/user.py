import datetime

from flask import request, Blueprint
from marshmallow import ValidationError
import jwt

from utils.schema import CreateUserInputSchema
from utils.log import log_and_capture
from utils.block import BLOCKLIST
from utils.auth import key, jwt_required
from models.user import UserModel

auth_schema = CreateUserInputSchema()
user_page = Blueprint("user_page", __name__)


@user_page.route("/register", methods=["POST"], endpoint="sign_up")
@log_and_capture(endpoint="sign_up")
def post():
    # Validate information on the request body
    info = request.json
    try:
        data = auth_schema.load(info)
    except ValidationError as e:
        return str(e.messages), 400
    if UserModel.find_by_username(data["username"]):
        return {"msg": "An user with that username already exists."}, 400

    # Handle the request of creating a new user
    user = UserModel(**data)
    user.save_to_db()
    return {"msg": "User created successfully."}, 201


@user_page.route("/login", methods=["POST"], endpoint="sign_in")
@log_and_capture(endpoint="sign_in")
def post():
    # Handle the request of signing in

    # Validate information on the request body
    info = request.json
    try:
        data = auth_schema.load(info)
    except ValidationError as e:
        return str(e.messages), 400

    # Return a pair of token to access and refresh
    user = UserModel.find_by_username(data["username"])
    if user and (user.password == data["password"]):
        access_token = jwt.encode({"identity": user.id, "iat": datetime.datetime.utcnow()}, key, algorithm="HS256")
        return {"access_token": access_token}, 200
    return {"msg": "Please register first!"}, 401


@user_page.route("/logout", methods=["POST"], endpoint="sign_out")
@log_and_capture(endpoint="sign_out")
@jwt_required
def post(**token):
    # Handle the request of signing out by adding the present token to block list
    BLOCKLIST.add(str(token["iat"]))
    return {"msg": "Successfully logged out!"}, 200
