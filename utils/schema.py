from marshmallow import Schema, fields, post_load, ValidationError


class ItemSchema(Schema):
    # Schema used to transform an item object to json
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    category_id = fields.Int()
    user_id = fields.Int()


class GetItemListSchema(Schema):
    # Schema to validate info to get a list of items
    prefix = fields.Str(missing="")
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=5)

    @post_load()
    def validate_page(self, data, **kwargs):
        if data['page'] < 1:
            raise ValidationError("The page number has to be positive.")


class CreateUserInputSchema(Schema):
    # Schema to validate info to create an user object
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ItemInputSchema(Schema):
    # Schema to validate info to create an item object
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category = fields.Str(required=True)
