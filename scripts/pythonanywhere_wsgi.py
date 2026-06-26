# =============================================================================
# PythonAnywhere WSGI configuration
# Copy this into:  Web tab → WSGI configuration file
# Replace YOURUSERNAME with your PythonAnywhere username (3 places).
# =============================================================================

import os
import sys

# Project path on PythonAnywhere
path = '/home/YOURUSERNAME/zebib'
if path not in sys.path:
    sys.path.insert(0, path)

# Production settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

# Load .env (django-environ reads it from BASE_DIR)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
