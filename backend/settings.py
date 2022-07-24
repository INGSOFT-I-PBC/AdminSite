"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Module for load environment variables from .env file
import environ
import os

env = environ.Env()
environ.Env.read_env(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [env("APP_URL"), env("APP_HOST")]

if DEBUG:
    # Prevent CORS on debug mode
    ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # 'drf_yasg',
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
ENGINES = {
    "postgres": "django.db.backends.postgresql",
    "mysql": "django.db.backends.mysql",
    "sqlite": "django.db.backends.sqlite3",
    "oracle": "django.db.backends.oracle",
}

DATABASES = {
    "default": {
        "ENGINE": ENGINES[env("DB_ENGINE")],
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TEST": {
            "NAME": "staging",
        },
    },
    "users": {
        "ENGINE": ENGINES[env("DB_ENGINE")],
        "NAME": "users",
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TEST": {
            "NAME": "staging",
        },
    },
    "session": {
        "ENGINE": ENGINES[env("DB_ENGINE")],
        "NAME": "session",
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "TEST": {
            "NAME": "staging",
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Logging Settings
LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "production_mode": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "console": {"level": "INFO", "filters": ["require_debug_true"], "class": "logging.StreamHandler"},
        "query_log": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "backend/storage/logs/django_query.log",
        },
        "logfile": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "backend/storage/logs/django.log",
        },
    },
    "loggers": {
        "django.db.backends": {"level": "DEBUG", "handlers": ["query_log"]},
        "django": {"level": "WARNING", "handlers": ["logfile"]},
    },
}

# File Upload Settings
# Setting as: 20 MiB
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520

# JWT Rest Framework settings

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "COMPACT_JSON": True,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
    ),
}


def read_key(path):
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    raise Exception(f"No keyfile was found (at:{os.path.realpath(path)})")


def get_key(public: bool = True):
    try:
        if public:
            return read_key("backend/storage/jwt/public.pem")
        else:
            return read_key("backend/storage/jwt/private.pem")
    except Exception:
        return env("JWT_PUBLIC_KEY") if public else env("JWT_PRIVATE_KEY")


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "RS256",
    "TOKEN_USER_CLASS": "api.models.User",
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "SIGNING_KEY": get_key(public=False),
    "VERIFYING_KEY": get_key(),
}

# Authentication Settings

LOGIN_URL = "/api/v1/login"
LOGOUT_URL = "/api/v1/logout"

AUTH_USER_MODEL = "api.User"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
