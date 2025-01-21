import asyncio
import csv
import logging
import os

from tortoise import Tortoise

from config import DB_NAME, FILES_DIR, DOMAIN_FILE
from models import Domain


async def init_db():
    await Tortoise.init(
        db_url=f"sqlite://database/{DB_NAME}", modules={"models": ["models"]}
    )
    logging.info("Initializing database...")


async def close_db():
    await Tortoise.close_connections()


async def create_schema():
    await Tortoise.generate_schemas()
    logging.info("Database schema created.")


async def populate_data():
    file_path = str(get_file_path())
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".txt":
        await _populate_from_txt(file_path)
    elif file_extension == ".csv":
        await _populate_from_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


async def add_domain(url: str):
    if not url.startswith("https://"):
        url = "https://" + url
    if not await Domain.exists(url=url):
        # fixme bulk_create is faster?
        await Domain.create(url=url)
        logging.info(f"Domain added to db: {url}")


async def _populate_from_txt(file_path: str):
    with open(file_path, "r") as file:
        for line in file:
            url = line.strip()
            if url:
                try:
                    await add_domain(url)
                except Exception as ex:
                    logging.error(f"Error adding domain from txt: {url}, error: {ex}")
    logging.info(f"Data populated from txt file: {file_path}")


async def _populate_from_csv(file_path: str):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                url = row[0].strip()
                if url:
                    try:
                        await add_domain(url)
                    except Exception as ex:
                        logging.error(
                            f"Error adding domain from csv: {url}, error: {ex}"
                        )
    logging.info(f"Data populated from csv file: {file_path}")


def get_file_path():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, FILES_DIR, DOMAIN_FILE)
    return file_path


async def main():
    try:
        await init_db()
        await create_schema()
        await populate_data()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        await close_db()


# only for development mode!!!
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Unexpected exception: {repr(e)}")
