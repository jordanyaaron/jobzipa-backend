import os
from pathlib import Path
from decouple import config
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔥 SECURITY / BASIC
# =========================
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

AUTH_USER_MODEL = 'users.User'

# =========================
# 🔥 APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'apps.users',
    'apps.jobs',

    "corsheaders",  # 🔥 IMPORTANT
]

# =========================
# 🔥 MIDDLEWARE (FIXED ORDER)
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 🔥 MUST BE FIRST
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# 🔥 CORS CONFIG
# =========================

CORS_ALLOWED_ORIGINS = [
    "https://jobzipa.com",
    "https://www.jobzipa.com",
    "https://jobzipa-frontend.vercel.app",
    "https://prototype.jobzipa.com",
    "https://jobzipa-frontend.onrender.com",
]

# 🔥 TEMP DEBUG (REMOVE LATER IN PROD IF YOU WANT STRICT SECURITY)
# CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_HEADERS = ["*"]

# =========================
# 🔥 DATABASE
# =========================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL")
    )
}

# =========================
# 🔥 REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# =========================
# 🔥 JWT
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# =========================
# 🔥 STATIC / MEDIA
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# 🔥 INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'