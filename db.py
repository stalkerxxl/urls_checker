from tortoise.models import Model
from tortoise import fields, Tortoise


class Domain(Model):
    url = fields.CharField(primary_key=True, max_length=255)
    ok_count = fields.IntField(default=0)
    error_count = fields.IntField(default=0)
    last_error = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


async def db_init():
    await Tortoise.init(
        db_url="sqlite://database/db.sqlite3", modules={"models": ["db"]}
    )
    await Tortoise.generate_schemas()
