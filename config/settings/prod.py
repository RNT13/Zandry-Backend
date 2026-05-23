import os

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", ".up.railway.app").split()

FRONTEND_URL = os.getenv("FRONTEND_URL", "https://zandry.vercel.app")

CORS_ALLOWED_ORIGINS = [FRONTEND_URL] if FRONTEND_URL else []
CSRF_TRUSTED_ORIGINS = [FRONTEND_URL] if FRONTEND_URL else []

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
