from marshmallow import Schema, fields

class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phoneNumber = fields.Str(required=True)
    photoUrl = fields.Str(required=True)
    postsCount = fields.Integer(required=True)
