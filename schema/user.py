from marshmallow import Schema, fields


class CreateUserInputSchema(Schema):
    """ Schema to validate info to create an user object """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
