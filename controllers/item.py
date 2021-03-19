from flask import request, Blueprint
from marshmallow import ValidationError

from models.item import ItemModel, CategoryModel
from utils.schema import ItemSchema, ItemInputSchema, GetItemListSchema
from utils.log import log_and_capture
from utils.auth import jwt_required

"""Schema used to return a json representation of an item object """
item_schema = ItemSchema()
item_page = Blueprint("item_page", __name__)


@item_page.route("/items/<int:id>", methods=["GET"], endpoint="item_detail")
@log_and_capture(endpoint="item_detail")
def get(id):
    # Handles the request of getting an item
    item = ItemModel.find_by_id(id)
    print(item)
    if item:
        return item_schema.dump(item), 200
    return {"msg": "Item not found!"}, 404


@item_page.route("/items/<int:id>", methods=["DELETE"], endpoint="item_delete")
@log_and_capture(endpoint="item_delete")
@jwt_required
def delete(id, **token):
    # Handles the request of deleting an item from its owner or an admin
    user_identity = token["identity"]
    item = ItemModel.find_by_id(id)

    if item.user_id != user_identity:
        return {"msg": "You need to be the owner!"}, 400
    if item:
        try:
            item.delete_from_db()
        except RuntimeError:
            return {"msg": "An error occurred deleting the item."}, 500
    return {"msg": "Item deleted!"}


@item_page.route("/items/<int:id>", methods=["PUT"], endpoint="item_edit")
@log_and_capture(endpoint="item_edit")
@jwt_required
def put(id, **token):
    # Handles the request of updating an item from its owner or an admin

    # Get the id of the request sender from JWT
    user_identity = token["identity"]
    item = ItemModel.find_by_id(id)

    # Validate information on the request body
    create_item_schema = ItemInputSchema()
    info = request.json
    try:
        data = create_item_schema.load(info)
    except ValidationError as e:
        return str(e.messages), 400

    # Create a new category if necessary for the item
    category = CategoryModel.find_by_name(data["category"])
    if not category:
        category = CategoryModel(data["category"])
        category.save_to_db()
    data["category"] = category.id

    # Only update an existing item
    if item:
        if item.user_id != user_identity:
            return {"msg": "You need to be the owner!"}, 400
        item.update_to_db(**data)
    else:
        return {"msg": "Item not found!"}, 404
    return {"msg": "Item updated!"}


@item_page.route("/items", methods=["GET"], endpoint="item_list")
@log_and_capture(endpoint="item_list")
def get():
    # Handle the request of getting a list of items

    # Validate information on the query string
    info = request.args
    item_list_schema = GetItemListSchema()
    try:
        data = item_list_schema.load(info)
    except ValidationError as e:
        return str(e.messages), 400

    # Only get one page of items
    if data:
        pagination = ItemModel.pagination(data["prefix"], data["per_page"], data["page"])
        if pagination:
            return {"items": list(map(lambda x: item_schema.dump(x), pagination))}
    return {"items": []}


@item_page.route("/items", methods=["POST"], endpoint="item_add")
@jwt_required
@log_and_capture(endpoint="item_add")
def post(**token):
    # Handle the request of creating a new item
    user_id = token["identity"]

    # Validate information on the request body
    create_item_schema = ItemInputSchema()
    info = request.json
    try:
        data = create_item_schema.load(info)
    except ValidationError as e:
        return str(e.messages), 400

    # Create a new category if necessary for the new item
    category = CategoryModel.find_by_name(data["category"])
    if not category:
        category = CategoryModel(data["category"])
        category.save_to_db()
    data["category"] = category.id

    # Create the item
    item = ItemModel(**data, user=user_id)
    try:
        item.save_to_db()
    except RuntimeError:
        return {"msg": "An error occurred creating the item!"}, 500
    return item_schema.dump(item), 201
