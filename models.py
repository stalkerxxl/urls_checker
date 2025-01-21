import logging

from tortoise import Model, fields


class Domain(Model):
    # fixme добавить проверку на валидность url
    url = fields.CharField(primary_key=True, max_length=255)
    ok_count = fields.IntField(default=0)
    error_count = fields.IntField(default=0)
    last_error = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @staticmethod
    async def get_all_urls():
        logging.info("Getting all urls from database")
        return await Domain.all().values_list("url", flat=True)

    @staticmethod
    async def increment_ok(url):
        domain = await Domain.get_or_none(url=url)
        if domain:
            domain.ok_count += 1
            await domain.save()

    @staticmethod
    async def increment_error(url, error):
        domain = await Domain.get_or_none(url=url)
        if domain:
            domain.error_count += 1
            domain.last_error = error
            await domain.save()
