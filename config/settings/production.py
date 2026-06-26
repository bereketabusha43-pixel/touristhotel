"""Production settings for PythonAnywhere deployment."""
from .base import *  # noqa: F403, F401

DEBUG = False

# PythonAnywhere terminates SSL at the proxy — required for HTTPS detection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SSL / security (disable SECURE_SSL_REDIRECT on PA if you get redirect loops)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF — set your full site URL in .env
CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=[SITE_URL] if SITE_URL.startswith('https') else [],  # noqa: F405
)

# Static files — reliable storage for deployment (no manifest hash issues)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Logging — surface errors in PythonAnywhere error log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='WARNING'),
            'propagate': False,
        },
    },
}
