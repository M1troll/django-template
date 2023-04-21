import environ

from .common import *

env = environ.Env()

env.read_env()

DEBUG = env.bool("DEBUG", default=False)

# ------------------------------------------------------------------------------
# DATABASES - PostgreSQL
# ------------------------------------------------------------------------------
DATABASES["default"].update(
    NAME=env.str("DATABASE_NAME"),
    USER=env.str("POSTGRES_USER"),
    PASSWORD=env.str("POSTGRES_PASSWORD"),
    HOST=env.str("POSTGRES_HOST"),
    PORT=env.int("POSTGRES_PORT"),
)

# ------------------------------------------------------------------------------
# DJANGO SECURITY
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# ------------------------------------------------------------------------------
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["*"]
