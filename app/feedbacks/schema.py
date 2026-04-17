from marshmallow import Schema, fields

class CreateFeedback(Schema):
    message = fields.Str(required=True)
    rating = fields.Integer(required=True)


class CompactedUser(Schema):
    name = fields.Str(required=True)
    photoUrl = fields.Email(required=True)

class GetFeedback(Schema):
    message = fields.Str(required=True)
    rating = fields.Integer(required=True)
    created = fields.DateTime(required=True)
    user = fields.Nested(CompactedUser, required=True)