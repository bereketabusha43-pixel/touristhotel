"""Development settings."""
from .base import *  # noqa: F403, F401

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Use simple static storage in development
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

INTERNAL_IPS = ['127.0.0.1']
