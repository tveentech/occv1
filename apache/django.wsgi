import os
import sys

sys.path.append('/var/live_code/planbaba/occv1')

os.environ['PYTHON_EGG_CACHE'] = '/var/live_code/planbaba/occv1/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'occv1.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
