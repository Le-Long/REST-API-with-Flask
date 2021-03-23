from marshmallow import Schema, fields, validate


class ValidateUserInputSchema(Schema):
    """Schema to validate info to create an user or log in as one"""
    username = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))
