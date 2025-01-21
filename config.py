import logging
import decouple

DEBUG = decouple.config("DEBUG", cast=bool)

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOG_LEVEL)

DB_NAME=decouple.config("DB_NAME", cast=str)