from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Str(dump_only=True)
    reportId = fields.Str(required=True)
    content = fields.Str(required=True)
    userId = fields.Str(dump_only=True)
    userName = fields.Str(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    parentId = fields.Str(required=True, allow_none=True)
