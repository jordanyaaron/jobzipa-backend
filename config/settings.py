import os
from pathlib import Path
from decouple import config
import dj_database_url
from datetime import timedelta

ROOT_URLCONF = 'config.urls'

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# 🔥 SECURITY / BASIC
# =========================
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

AUTH_USER_MODEL = 'users.User'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = config("DEBUG", default=False, cast=bool)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
FRONTEND_WEB_APP_NAME="Jobzipa"

# superuser info
DJANGO_SUPERUSER_USERNAME=config('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_EMAIL=config('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_PASSWORD=config('DJANGO_SUPERUSER_PASSWORD')

# amazon
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")
AWS_S3_BUCKET_NAME = config("AWS_S3_BUCKET_NAME")
AWS_S3_BASE_URL = config("AWS_S3_BASE_URL")

# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")



FRONTEND_URL=config("FRONTEND_URL")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

AUTH_USER_MODEL = 'users.User'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")
AWS_S3_BUCKET_NAME = config("AWS_S3_BUCKET_NAME")
# Application definition

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
CORS_ALLOW_ALL_ORIGINS = True 

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