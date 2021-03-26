from marshmallow import Schema, fields, post_load, validate, ValidationError

from schema.category import CategorySchema


class ItemSchema(Schema):
    """Schema used to transform an item object to a dictionary"""
    id = fields.Int()
    name = fields.Str(required=True, validate=validate.Length(max=80))
    price = fields.Float(required=True)
    category = fields.Nested(CategorySchema, only=("name",))
    user_id = fields.Int()


class GetItemListSchema(Schema):
    """Schema to validate info to get a list of items"""
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
