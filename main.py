import asyncio
import logging

from db import init_db, create_schema, close_db, populate_data


async def main():
    try:
        await init_db()
        await create_schema()
        await populate_data()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Error in main", exc_info=e)
