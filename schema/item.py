from marshmallow import Schema, fields, post_load, post_dump, ValidationError
from models.item import CategoryModel


class ItemSchema(Schema):
    """ Schema used to transform an item object to json """
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    category_id = fields.Int()
    user_id = fields.Int()

    @post_dump()
    def get_category(self, info, **kwargs):
        category = CategoryModel.find_by_id(info["category_id"])
        del info["category_id"]
        info["category"] = category.name
        return info


class GetItemListSchema(Schema):
    """ Schema to validate info to get a list of items """
    name = fields.Str(missing="")
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=5)

    @post_load()
    def validate_page(self, data, **kwargs):
        # Custom validation to ensure page number is positive
        if data["page"] < 1:
            raise ValidationError("The page number has to be positive.")
        if data["per_page"] < 1:
            raise ValidationError("The number of items per page has to be positive.")
        return data


class ItemInputSchema(Schema):
    """ Schema to validate info to create an item object """
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category = fields.Str(required=True)
