"""
ASGI config for library_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

prod = os.environ.get('PROD', False)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', ('library_management.settings.prod' if prod else 'library_management.settings.dev'))

application = get_asgi_application()
