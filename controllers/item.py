from flask import request, Blueprint

from models.item import ItemModel
from models.category import CategoryModel
from schema.item import ItemSchema, GetItemListSchema
from utils.log import log_and_capture
from utils.auth import jwt_required

# Schema used to return a json representation of an item object
item_schema = ItemSchema()

item_page = Blueprint("item_page", __name__)


def validate_item_input(param, schema):
    """Validate information on the request"""
    schema_obj = schema()
    data = schema_obj.load(param)
    return data


@item_page.route("/items/<int:id>", methods=["GET"], endpoint="item_detail")
@log_and_capture(endpoint="item_detail")
def get(id):
    """Handles the request of getting an item

    Arguments:
    id: int
        the identity of the item

    Return:
    Item if success: JSON
        format {
                "id": int,
                "name": str,
                "price": float,
                "category_id": int,
                "user_id": int
                }
    Message if error: dictionary
        format {"msg": "Item not found!"}
    Status code: int
        200 if OK
        404 if item not found
    """

    item = ItemModel.find_by_id(id)
    if item:
        return item_schema.dump(item), 200
    return {"msg": "Item not found!"}, 404


@item_page.route("/items/<int:id>", methods=["DELETE"], endpoint="item_delete")
@log_and_capture(endpoint="item_delete")
@jwt_required
def delete(id, **token):
    """Handles the request of deleting an item from its owner

    Arguments:
    id: int
        the index of the item user want to delete
    Token: dictionary
        format {"identity": user id, "iat": the time the token was created}

    Return:
    Message if success: dictionary
        format {"msg": "Item deleted!"}
    Message if error: dictionary
        format {"msg": The error message}
    Status code: int
        200 if OK
        403 if user is not the owner
        404 if item not found
    """
    user_identity = token["identity"]
    item = ItemModel.find_by_id(id)

    if not item:
        return {"msg": "Item not found!"}, 404
    if item.user_id != user_identity:
        return {"msg": "You need to be the owner!"}, 403
    item.delete_from_db()
    return {"msg": "Item deleted!"}, 200


@item_page.route("/items/<int:id>", methods=["PUT"], endpoint="item_edit")
@log_and_capture(endpoint="item_edit")
@jwt_required
def put(id, **token):
    """Handles the request of updating an item from its owner

    If the item has a new category we create that category too.

    Arguments:
    id: int
        the index of the item user want to update
    Token: dictionary
        format {"identity": user id, "iat": the time the token was created}

    Return:
    Message if success: dictionary
        format {"msg": "Item updated!"}
    Message if error: dictionary
        format {"msg": The error message}
    Status code: int
        200 if OK
        403 if user is not the owner
        404 if item not found
    """

    # Get the id of the request sender from JWT
    user_identity = token["identity"]
    item = ItemModel.find_by_id(id)

    # Validate information on the request body
    data = validate_item_input(request.json, ItemSchema)

    # Only update an existing item
    if item:
        if item.user_id != user_identity:
            return {"msg": "You need to be the owner!"}, 403

        # Create a new category if necessary for the item
        category = CategoryModel.find_by_name(data["category"]["name"])
        if not category:
            category = CategoryModel(data["category"]["name"])
        category.save_to_db()

        data["category"] = category.id
        item.update_to_db(**data)

    else:
        return {"msg": "Item not found!"}, 404
    return {"msg": "Item updated!"}, 200


@item_page.route("/items", methods=["GET"], endpoint="item_list")
@log_and_capture(endpoint="item_list")
def get():
    """Handles the request of getting a list of items

    Arguments:
    id: int
        the index of the item user want to get

    Return:
    Item list: JSON
        format {"items":
                    [
                    {"id":int,
                    "name": str contains <name>,
                    "price":float,
                    "category_id":int,
                    "user_id":int},
                    ],
                "prev_page": bool,
                "next_page": bool
                }
    Status code: int
        200 if OK
    """

    # Validate information on the query string
    data = validate_item_input(request.args, GetItemListSchema)

    # Only get one page of items
    query = ItemModel.query_with_condition(ItemModel.name.contains(data["name"]))
    pagination, number_of_page = ItemModel.paginate(query, data["per_page"], data["page"])
    if not pagination:
        item_list = []
    else:
        item_list = list(map(lambda x: item_schema.dump(x), pagination))
    return {"items": item_list,
            "current_page": data["page"],
            "number_of_page": number_of_page}, 200


@item_page.route("/items", methods=["POST"], endpoint="item_add")
@log_and_capture(endpoint="item_add")
@jwt_required
def post(**token):
    """Handle the request of creating a new item

    If the new item has a new category we create that category too.

    Arguments:
    Token: dictionary
        format {"identity": user id, "iat": the time the token was created}

    Return:
    Item if success: JSON
        format {
                "id":int,
                "name": str,
                "price":float,
                "category_id":int,
                "user_id":int
                }
    Status code: int
        201 if OK
    """

    user_id = token["identity"]

    # Validate information on the request body
    data = validate_item_input(request.json, ItemSchema)

    # Create a new category if necessary for the new item
    category = CategoryModel.find_by_name(data["category"]["name"])
    if not category:
        category = CategoryModel(data["category"]["name"])
        category.save_to_db()

    data["category"] = category.id

    # Create the item
    item = ItemModel(**data, user_id=user_id)
    item.save_to_db()

    return item_schema.dump(item), 201
