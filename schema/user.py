from marshmallow import Schema, fields


class ValidateUserInputSchema(Schema):
    """ Schema to validate info to create an user or log in as one """
    username = fields.Str(required=True)
    password = fields.Str(required=True)
