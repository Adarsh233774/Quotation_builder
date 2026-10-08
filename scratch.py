import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
from django.conf import settings
settings.ALLOWED_HOSTS = ['*']
django.setup()
from django.test import Client

try:
    c = Client(HTTP_HX_REQUEST='true', HTTP_HX_TRIGGER_NAME='calculation_type')
    c.post('/quotations/items/1/htmx/update/', {'calculation_type': 'FIXED', 'rate': '4.99', 'amount': '4.99'})
    r = c.post('/quotations/items/1/htmx/update/', {'calculation_type': 'AREA_RATE', 'rate': '4.99', 'amount': '4.99'})
    print(r.status_code)
    print(r.content.decode())
except Exception as e:
    traceback.print_exc()
