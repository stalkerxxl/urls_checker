import asyncio
import logging
import time
import tracemalloc

import aiohttp
from aiohttp import ClientTimeout

from config import MAX_CONCURRENT_TASKS, TOTAL_TIMEOUT, SOCK_CONNECT_TIMEOUT
from db import init_db, create_schema, close_db, populate_data
from models import Domain

ok = 0
errors = 0


async def fetch(session, url, semaphore):
    global ok, errors
    async with semaphore:
        try:
            async with session.get(
                url,
                timeout=ClientTimeout(
                    total=TOTAL_TIMEOUT, sock_connect=SOCK_CONNECT_TIMEOUT
                ),
                raise_for_status=True,
            ) as response:
                status = response.status
                ok += 1
                logging.debug(f"{url=}, {status}")
                await Domain.increment_ok(url)
        except Exception as ex:
            errors += 1
            await Domain.increment_error(url, ex)
            logging.error(f"Error fetching {url}: {ex}")


async def fetch_all(urls):
    logging.info("Fetching all urls...")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    start_time = time.perf_counter()
    tracemalloc.start()
    try:
        await init_db()
        await create_schema()
        await populate_data()

        urls = await Domain.get_all_urls()
        await fetch_all(urls)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter()

        print(f"{MAX_CONCURRENT_TASKS=}, {TOTAL_TIMEOUT=}, {SOCK_CONNECT_TIMEOUT=}")
        print(f"Processed {ok + errors} URLs in {end_time - start_time:.2f} seconds")
        print(f"OK: {ok}, ERRORS: {errors}")
        print(
            f"Average response time: {(end_time - start_time) / (ok + errors):.2f} seconds"
        )
        print(f"Current Memory Usage: {current / 1024 / 1024:.2f} MB")
        print(f"Peak Memory Usage: {peak / 1024 / 1024:.2f} MB")
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception("Unexpected ERROR", exc_info=e)
