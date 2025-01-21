from tortoise import Model, fields


class Domain(Model):
    url = fields.CharField(primary_key=True, max_length=255)
    ok_count = fields.IntField(default=0)
    error_count = fields.IntField(default=0)
    last_error = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
