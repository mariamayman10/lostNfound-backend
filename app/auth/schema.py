from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    uid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phoneNumber = fields.Str(required=True, validate=validate.Regexp(r"^\+9665\d{8}$"))
    photoUrl = fields.Str()
    postsCount = fields.Int(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)

class RegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phoneNumber = fields.Str(required=True, validate=validate.Regexp(r"^\+9665\d{8}$"))
    password = fields.Str(required=True, load_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
