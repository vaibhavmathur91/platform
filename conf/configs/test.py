"""
Streamlined Django settings for running test cases.
"""

import logging
import os

from .common import DEFAULT_TEMPLATE_CONTEXT_PROCESSORS, DEFAULT_MIDDLEWARE_CLASSES, DEFAULT_INSTALLED_APPS, PIPELINE

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '0.5.0'

# Define the base working directory of the application
BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))

# Application definition

INSTALLED_APPS = DEFAULT_INSTALLED_APPS

MIDDLEWARE_CLASSES = DEFAULT_MIDDLEWARE_CLASSES

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS

# This is an insecure password hasher, but much faster than what would be used in production
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Security

CSRF_MIDDLEWARE_SECRET = None

# Logging

DEBUG = False
TEMPLATE_DEBUG = False

if os.environ.get('TEST_DEBUG', 'False') == 'True':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'WARN',
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'helium': {
                'handlers': ['console'],
                'level': 'DEBUG',
            }
        }
    }
else:
    logging.disable(logging.ERROR)

# Database configuration

if os.environ.get('USE_IN_MEMORY_DB', 'True') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.test.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'NAME': os.environ.get('PLATFORM_DB_NAME'),
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.environ.get('PLATFORM_DB_HOST'),
            'USER': os.environ.get('PLATFORM_DB_USER'),
            'PASSWORD': os.environ.get('PLATFORM_DB_PASSWORD'),
        }
    }

# Static

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# Pipelines

PIPELINE['CSS_COMPRESSOR'] = None
PIPELINE['JS_COMPRESSOR'] = None

# Celery

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# StatsD

STATSD_PORT = 0