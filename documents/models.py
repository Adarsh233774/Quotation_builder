from django.db import models
from quotations.models import Quotation

class DocumentSnapshot(models.Model):
    DOCUMENT_TYPES = [
        ('PDF', 'PDF Document'),
        ('DOCX', 'Word Document'),
        ('EXCEL', 'Excel Workbook'),
    ]

    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='quotation_documents/')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.document_type} ({self.created_at.strftime('%Y-%m-%d')})"
