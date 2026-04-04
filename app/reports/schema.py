from marshmallow import Schema, fields

class BaseReportSchema(Schema):
    id = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    location = fields.Str(required=True)
    category = fields.Str(required=True)
    status = fields.Str(required=True)
    type = fields.Str(required=True)
    imageUrls = fields.List(fields.Str)
    createdAt = fields.DateTime(required=True)
    userId = fields.Str(required=True)

class ReportSchema(BaseReportSchema):
    pass

class GetReportSchema(BaseReportSchema):
    isOwner = fields.Bool()
    userName = fields.Str()

class CreateReportSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    location = fields.Str(required=True)
    category = fields.Str(required=True)
    type = fields.Str(required=True)

class UpdateReportSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    location = fields.Str()