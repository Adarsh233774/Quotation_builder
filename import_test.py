import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from clients.models import Client
from projects.models import Project
from quotations.services.excel_import import import_excel_quotation

project = Project.objects.first()

if project:
    try:
        q = import_excel_quotation(
            filepath=r'D:\MY\Dad Work\Common Temp.xlsx',
            project=project,
            quotation_number='QTN/2026/IMPORT1',
            date=datetime.date.today()
        )
        print(f"Successfully imported {q.quotation_number} with Total Amount: Rs. {q.total_amount}")
        print("Sections imported:")
        for section in q.sections.all():
            print(f"- {section.name}: Rs. {section.section_total} ({section.items.count()} items)")
    except Exception as e:
        print(f"Error importing: {e}")
else:
    print("No project found to attach quotation to.")
