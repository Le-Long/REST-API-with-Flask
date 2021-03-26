import re

from marshmallow import Schema, fields, validate, validates, ValidationError


class ValidateRegisterSchema(Schema):
    """Schema to validate info to create an user or log in as one"""
    username = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    password = fields.Str(required=True)

    @validates("password")
    def validate_password(self, password):
        if len(password) < 5 or len(password) > 20:
            raise ValidationError("Length must be between 5 and 20.")
        if not re.match(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])', password):
            raise ValidationError(
                "Must contain at least one lowercase letter, "
                "one uppercase letter and one digit."
            )


class ValidateLoginSchema(Schema):
    """Schema to validate info to create an user or log in as one"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)
