import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quotations.models import Quotation
from quotations.services.excel_export import export_quotation_to_excel
from quotations.services.docx_generator import generate_docx_quotation

q = Quotation.objects.get(quotation_number='QTN/2026/IMPORT1')

# Export to Excel
excel_path = os.path.join(os.getcwd(), 'Exported_Quotation.xlsx')
export_quotation_to_excel(q, excel_path)
print(f"Exported Excel to {excel_path}")

# Export to DOCX
docx_path = os.path.join(os.getcwd(), 'Exported_Quotation.docx')
generate_docx_quotation(q, docx_path)
print(f"Exported Word to {docx_path}")
