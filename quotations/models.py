from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('REVIEW', 'Review'),
        ('APPROVED', 'Approved'),
        ('SENT', 'Sent'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
        ('ARCHIVED', 'Archived'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='quotations')
    quotation_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    prepared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prepared_quotations')
    version = models.IntegerField(default=1)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    additional_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quotation_number

class QuotationSection(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    section_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.name}"

class QuotationItem(models.Model):
    CALCULATION_TYPES = [
        ('FIXED', 'Fixed Amount'),
        ('QTY_RATE', 'Quantity \u00d7 Rate'),
        ('AREA_RATE', 'Length \u00d7 Width \u00d7 Rate'),
        ('CUSTOM_AREA', 'Custom Area \u00d7 Rate'),
    ]

    section = models.ForeignKey(QuotationSection, on_delete=models.CASCADE, related_name='items')
    description = models.TextField(blank=True, null=True)
    specification = models.TextField(blank=True, null=True)
    
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES, default='AREA_RATE')
    
    length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit = models.CharField(max_length=50, blank=True, null=True, default='Sq.ft')
    
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    remarks = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.description or "Item"

class QuotationVersion(models.Model):
    original_quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    snapshot_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
