"""
Django settings for nefarious project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v5&#^pw*5_$lq87j$92z54f=#s@fv+4xqfjwoo9++n#l+3!0$@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nefarious.apps.AppConfig',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
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
]

ROOT_URLCONF = 'nefarious.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# https://github.com/kennethreitz/dj-database-url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:////{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticassets"),
]
STATIC_ROOT = "staticfiles"


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{host}:{port}/0".format(host=REDIS_HOST, port=REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

WEBSOCKET_URL = os.environ.get('WEBSOCKET_HOST', 'ws://nefarious:80/ws')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # session auth is really only for browsing the api when you're already logged into the admin
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': None,
}

#
# The Movie Database
# https://developers.themoviedb.org/3/getting-started/introduction
#

# rate limiting is supposedly per IP address (not per token) so this should be safe to use across all installations.
# UPDATE: As of Dec 16, 2019 rate limiting is no longer enforced.
# https://developers.themoviedb.org/3/getting-started/request-rate-limiting
TMDB_API_TOKEN = '21c8985a267ac3f11ea75baf2c05c3ba'

# OpenSubtitles - this is only the api key; authenticated users get 100 subtitles/day
# https://opensubtitles.stoplight.io/docs/opensubtitles-api/open_api.json
OPENSUBTITLES_API_KEY = 'LG7LMRIL9zfVmF537mxnQDEfN4V7LLqX'

UNPROCESSED_PATH = '.nefarious-unprocessed-downloads'

# container download path (or will be host in development)
INTERNAL_DOWNLOAD_PATH = os.environ.get('INTERNAL_DOWNLOAD_PATH', '/tmp')

# this is really just an indication to know if the nefarious container was volume mounted with access to the download path.
# nefarious (celery) will actually use the INTERNAL_DOWNLOAD_PATH (container specific path) to scan for imported media
HOST_DOWNLOAD_PATH = os.environ.get('HOST_DOWNLOAD_PATH', INTERNAL_DOWNLOAD_PATH if DEBUG else None)

CONFIG_PATH = os.environ.get('CONFIG_PATH', '/nefarious-db')

# log to shared config path when using default container configuration, otherwise fallback to /tmp
log_path = CONFIG_PATH if os.path.exists(CONFIG_PATH) else '/tmp'
NEFARIOUS_LOG_FILE_FOREGROUND = os.path.join(log_path, '.foreground.log')
NEFARIOUS_LOG_FILE_BACKGROUND = os.path.join(log_path, '.background.log')

MAX_LOG_BYTES = 1024 ** 2 * 5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s '
                      '%(process)d  %(thread)d  %(message)s'
        },
    },
    "handlers": {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file-background': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': NEFARIOUS_LOG_FILE_BACKGROUND,
            'maxBytes': MAX_LOG_BYTES,
            'backupCount': 1,  # only keep a single backup which gets overwritten during rotation
        },
        'file-foreground': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': NEFARIOUS_LOG_FILE_FOREGROUND,
            'maxBytes': MAX_LOG_BYTES,
            'backupCount': 1,  # only keep a single backup which gets overwritten during rotation
        },
    },
    'loggers': {
        "nefarious-background": {
            "handlers": ["console", "file-background"],
            "level": "INFO",
        },
        "nefarious-foreground": {
            "handlers": ["console", "file-foreground"],
            "level": "INFO",
        },
    }
}