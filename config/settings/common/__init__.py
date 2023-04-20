# -----------------------------------------------------------------------------
# General Django Configuration Starts Here
# -----------------------------------------------------------------------------
from .authentication import *
from .databases import *
from .installed_apps import *
from .internationalization import *
from .middleware import *
from .paths import *
from .security import *
from .static import *
from .templates import *

# -----------------------------------------------------------------------------
# Business Logic Custom Variables and Settings
# -----------------------------------------------------------------------------
DEBUG = True
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

ADMINS = (
    ("Anton Oboleninov", "oboleninoff.anton@yandex.ru"),
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom settings
APP_LABEL = "Project Name"
