import socket

import environ

from .common import *

env = environ.Env()

env.read_env()

DEBUG = env.bool("DEBUG", default=False)

INTERNAL_IPS = (
    "0.0.0.0",
    "127.0.0.1",
)
# Hack to have working `debug` context processor when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += (ip[:-1] + "1",)

DATABASES["default"].update(
    NAME=env.str("DATABASE_NAME", ""),
    USER=env.str("POSTGRES_USER", ""),
    PASSWORD=env.str("POSTGRES_PASSWORD", ""),
    HOST=env.str("POSTGRES_HOST", ""),
    PORT=env.int("POSTGRES_PORT", 0),
    CONN_MAX_AGE=0,
)

# disable any password restrictions
AUTH_PASSWORD_VALIDATORS = []
