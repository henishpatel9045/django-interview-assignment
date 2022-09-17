"""
WSGI config for library_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

prod = os.environ.get('PROD', False)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', ('library_management.settings.prod' if prod else 'library_management.settings.dev'))

application = get_wsgi_application()
