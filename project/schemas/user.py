from marshmallow import fields, Schema


class UserSchema(Schema):

    id = fields.Int(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    favorite_genre = fields.Str(required=True)