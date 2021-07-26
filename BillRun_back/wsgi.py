"""
WSGI config for BillRun_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import urllib
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BillRun_back.settings')

application = get_wsgi_application()

# 1번
# import django.core.handlers.wsgi
# _application = django.core.handlers.wsgi.WSGIHandler()

# def application(environ, start_response):
#     environ['PATH_INFO'] = urllib.unquote(environ['REQUEST_URI'].split('/o/')[1])
#     return _application(environ, start_response)

# 2번
# request_uri = os.environ['REQUEST_URI']
# request_uri = os.re.sub(r'%2F', '%2F', request_uri, os.re.I)
# os.environ['PATH_INFO'] = urllib.unquote(request_uri)