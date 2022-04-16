from marshmallow import Schema, fields


class FavoriteMovieSchema(Schema):
    user_id = fields.Int(required=True)
    movie_id = fields.Int(required=True)