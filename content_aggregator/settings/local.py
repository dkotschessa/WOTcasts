from .base import *

STATIC_ROOT = ""
STATICFILES_DIRS = [BASE_DIR / "static"]

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
