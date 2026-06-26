"""
WSGI config for config project.
Set DJANGO_SETTINGS_MODULE=config.settings.production on PythonAnywhere.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
