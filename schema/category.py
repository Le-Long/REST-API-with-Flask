from marshmallow import Schema, fields, post_load, post_dump, validate, ValidationError


class CategorySchema(Schema):
    """Schema used to transform a category object to a dictionary"""
    id = fields.Int()
    name = fields.Str(required=True)

