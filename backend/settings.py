"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

from django.core.management.utils import get_random_secret_key
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'false').lower() in ('true', '1', 't')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'backend.canvas_app_explorer',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_mysql',
    'webpack_loader',
    'rest_framework',
    'pylti1p3.contrib.django.lti1p3_tool_config',
    'tinymce',
    'canvas_oauth.apps.CanvasOAuthConfig',
    'drf_spectacular'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'canvas_oauth.middleware.OAuthMiddleware',
    'csp.middleware.CSPMiddleware'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.canvas_app_explorer.context_processors.cae_globals'
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'canvas_app_explorer_local'),
        'USER': os.getenv('DB_USER', 'cae_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'cae_pw'),
        'HOST': os.getenv('DB_HOST', 'canvas_app_explorer_mysql'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci'
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend'),
)

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend/webpack-stats.json')
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DEFAULT_FILE_STORAGE = 'backend.canvas_app_explorer.storage_get_file.DatabaseFileStorage'


# So request works over the proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DB_CACHE_CONFIGS = os.getenv('DB_CACHE_CONFIGS',
                           {'CACHE_TTL': 600, 'BACKEND': 'django_mysql.cache.MySQLCache',
                            'LOCATION': 'canvas_app_explorer_cache',
                            'CACHE_KEY_PREFIX': 'app_explorer',
                            'CACHE_OPTIONS': {'COMPRESS_MIN_LENGTH': 5000, 'COMPRESS_LEVEL': 6}
                            })

CACHES = {
    'default': {
        'BACKEND': DB_CACHE_CONFIGS['BACKEND'],
        'LOCATION': DB_CACHE_CONFIGS['LOCATION'],
        'OPTIONS': DB_CACHE_CONFIGS['CACHE_OPTIONS'],
        "KEY_PREFIX": DB_CACHE_CONFIGS['CACHE_KEY_PREFIX'],
        "TIMEOUT": DB_CACHE_CONFIGS['CACHE_TTL']
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # Gunicorns logging format https://github.com/benoitc/gunicorn/blob/19.x/gunicorn/glogging.py
    'formatters': {
        "generic": {
            "format": "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'rules': {
            'handlers': ['console'],
            'propagate': False,
            'level': os.getenv('RULES_LOG_LEVEL', 'INFO'),
        },
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },

    },
    'root': {
        'level': os.getenv('ROOT_LOG_LEVEL', 'INFO'),
        'handlers': ['console']
    },
}

TINYMCE_DEFAULT_CONFIG = {
        'menubar': True,
        "plugins": "advlist,autolink,code,lists,link,anchor,insertdatetime,media,table,paste,wordcount",
        "toolbar": "formatselect | bold italic backcolor | "
            "bullist numlist outdent indent | removeformat | code | help",
        "default_link_target": "_blank",
    }

# OAuth Settings, get these from the environment
# TODO: Add some of these to the Django LTI model
CANVAS_OAUTH_CLIENT_ID = os.getenv('CANVAS_OAUTH_CLIENT_ID', 'canvas_app_explorer')
CANVAS_OAUTH_CLIENT_SECRET = os.getenv('CANVAS_OAUTH_CLIENT_SECRET', 'canvas_app_explorer')
CANVAS_OAUTH_CANVAS_DOMAIN = os.getenv('CANVAS_OAUTH_CANVAS_DOMAIN', 'canvas.instructure.com')
CANVAS_OAUTH_SCOPES = os.getenv('CANVAS_OAUTH_SCOPES', '').split(',')
CANVAS_OAUTH_TOKEN_EXPIRATION_BUFFER = os.getenv('CANVAS_OAUTH_TOKEN_EXPIRATION_BUFFER', timedelta())
CANVAS_OAUTH_ERROR_TEMPLATE = os.getenv('CANVAS_OAUTH_ERROR_TEMPLATE', 'canvas_app_explorer/oauth_error.html')

# These are mostly needed by Canvas but it should also be on in general
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", False)
if CSRF_COOKIE_SECURE:
    CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", [])
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Enables Proxies that set headers
    USE_X_FORWARDED_HOST = os.getenv('USE_X_FORWARDED_HOST', True)

# Set CSP_FRAME_SRC to the your Canvas domains
CSP_FRAME_ANCESTORS = ["'self'",] + os.getenv('CSP_FRAME_ANCESTORS', '').split(',')
# This is currently unsafe-inline because of PyLTI scripts. This may be fixed in the future.
CSP_SCRIPT_SRC = ["'self'", "https:", "'unsafe-inline'"]
CSP_IMG_SRC = ["'self'", "data:"]
CSP_FONT_SRC = ["'self'"]
# Allow inline styles. There are a few styles that come up in the report so it seems easier to just allow unsafe-inline here.
CSP_STYLE_SRC = ["'self'", "https:", "'unsafe-inline'"]

SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", 'None')
CSRF_COOKIE_SAMESITE = os.getenv("CSRF_COOKIE_SAMESITE", 'None')

LTI_CONFIG_DISABLE_DEPLOYMENT_ID_VALIDATION = os.getenv('LTI_CONFIG_DISABLE_DEPLOYMENT_ID_VALIDATION', False)
RANDOM_PASSWORD_DEFAULT_LENGTH = os.getenv('RANDOM_PASSWORD_DEFAULT_LENGTH', 32)

# DRF, Spectacular, etc.
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'backend.canvas_app_explorer.utils.custom_exception_handler'
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Canvas App Explorer API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

HELP_URL = os.getenv('HELP_URL', '')

TEST_API_KEY = os.getenv('TEST_API_KEY', '')
TEST_API_URL = os.getenv('TEST_API_URL', '')
TEST_COURSE_ID = os.getenv('TEST_COURSE_ID', 1)
