"""
WSGI config for MediTagProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
# from db_articles import save_db

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MediTagProject.settings')


# save_db()

application = get_wsgi_application()


# not a good practice but these will be replaced with my attributes in index.py
# from Tagapp.models import Article
