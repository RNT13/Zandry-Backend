import os

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1").split()

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://zandry.vercel.app")

CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
CSRF_TRUSTED_ORIGINS = [FRONTEND_URL]

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
