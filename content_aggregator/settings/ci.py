from .base import *

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Local
    "accounts",
    "podcasts.apps.PodcastsConfig",
    "apis.apps.ApisConfig",
    # Third party apps
    "django_apscheduler",
    "django_extensions",
    "rest_framework",
    "corsheaders",
]

SECRET_KEY = env("DJANGO_SECRET_KEY")
