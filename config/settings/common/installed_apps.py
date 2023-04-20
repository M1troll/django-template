# Application definition
INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
)

THIRD_PARTY = (
    "django_extensions",
)

LOCAL_APPS = (
    # "apps.",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + LOCAL_APPS
