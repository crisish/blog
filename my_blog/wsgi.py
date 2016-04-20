"""
WSGI config for my_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/tmp/.python-eggs")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
