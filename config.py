import logging

from decouple import config

DEBUG = config("DEBUG", cast=bool)

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOG_LEVEL)

DB_NAME = config("DB_NAME", cast=str)

FILES_DIR = config("FILES_DIR", cast=str)
DOMAIN_FILE = config("DOMAIN_FILE", cast=str)

MAX_CONCURRENT_TASKS = config("MAX_CONCURRENT_TASKS", cast=int)
TOTAL_TIMEOUT = config("TOTAL_TIMEOUT", cast=int)
SOCK_CONNECT_TIMEOUT = config("SOCK_CONNECT_TIMEOUT", cast=int)
