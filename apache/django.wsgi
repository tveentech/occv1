import os
import sys

sys.path.append('/var/live_code/planbaba/occv1')

os.environ['PYTHON_EGG_CACHE'] = '/var/live_code/planbaba/occv1/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'occv1.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
