import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from clients.models import Client
from projects.models import Project

client, _ = Client.objects.get_or_create(name='Example Client', company='Example Corp')
Project.objects.get_or_create(name='Luxury Villa', client=client, location='Mumbai')

print("Database seeded with sample Client and Project.")
