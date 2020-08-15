from marshmallow import Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        ordered = True


class JSONInput(BaseSchema):
    """
    JSONInput - marshmallow schema for JSON input
    """

    class Machine(BaseSchema):

        class Outlets(BaseSchema):
            count_n = fields.Integer(Required=True)

        outlets = fields.Nested(Outlets, Required=True)
        total_items_quantity = fields.Dict(
            keys=fields.Str(), values=fields.Float(), Required=True)
        beverages = fields.Dict(
            keys=fields.Str(), values=fields.Dict(
                keys=fields.Str(), values=fields.Float()), Required=True)

    machine = fields.Nested(Machine, Required=True)
