import asyncio

from db import db_init


async def main():
    await db_init()


if __name__ == "__main__":
    asyncio.run(main())
