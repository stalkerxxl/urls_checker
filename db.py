import logging

from tortoise.models import Model
from tortoise import fields, Tortoise

from config import DB_NAME


class Domain(Model):
    url = fields.CharField(primary_key=True, max_length=255)
    ok_count = fields.IntField(default=0)
    error_count = fields.IntField(default=0)
    last_error = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


async def init_db():
    await Tortoise.init(
        db_url=f"sqlite://database/{DB_NAME}", modules={"models": ["db"]}
    )
    logging.info("Initializing database...")


async def close_db():
    await Tortoise.close_connections()


async def create_schema():
    await Tortoise.generate_schemas()
    logging.info("Database schema created.")
