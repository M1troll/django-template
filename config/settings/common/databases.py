from .paths import BASE_DIR

# ------------------------------------------------------------------------------
# DATABASES - PostgreSQL
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# ------------------------------------------------------------------------------

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "ATOMIC_REQUESTS": True,
#         "CONN_MAX_AGE": 600,
#     },
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
