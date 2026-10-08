from decimal import Decimal
from django.db import transaction

def parse_feet_inches(val):
    if not val:
        return Decimal('0')
    val_str = str(val).strip()
    if '.' not in val_str:
        return Decimal(val_str)
    
    parts = val_str.split('.')
    feet_str = parts[0]
    inches_str = parts[1]
    
    feet = Decimal(feet_str) if feet_str else Decimal('0')
    inches = Decimal(inches_str) if inches_str else Decimal('0')
    
    return feet + (inches / Decimal('12'))

def calculate_item(item):
    """
    Calculates the area and amount for a single QuotationItem.
    Updates the object but does NOT call save().
    """
    # Ensure standard Decimals
    qty = Decimal(str(item.quantity)) if item.quantity else Decimal('1')
    rate = Decimal(str(item.rate)) if item.rate else Decimal('0')

    if item.calculation_type == 'FIXED':
        # Amount is just rate (fixed price) or explicitly set amount
        item.area = Decimal('0')
        item.amount = Decimal(str(item.amount)) if getattr(item, '_manual_amount_override', False) else rate
    elif item.calculation_type == 'QTY_RATE':
        item.area = Decimal('0')
        item.amount = qty * rate
    elif item.calculation_type == 'AREA_RATE':
        length = parse_feet_inches(item.length)
        width = parse_feet_inches(item.width)
        area = length * width
        item.area = area
        item.amount = area * rate * qty
    elif item.calculation_type == 'CUSTOM_AREA':
        area = Decimal(str(item.area)) if item.area else Decimal('0')
        item.amount = area * rate * qty
    
    # Optional formatting for rounding, currently keep exact
    return item

def calculate_section(section):
    """
    Calculates the section total by aggregating all items.
    Updates the section object but does NOT call save().
    """
    total = Decimal('0')
    for item in section.items.all():
        calculate_item(item)
        item.save()
        total += item.amount
    
    section.section_total = total
    return section

@transaction.atomic
def calculate_quotation(quotation):
    """
    Calculates the subtotal, taxes, and total_amount for the entire quotation.
    Saves the entire hierarchy safely.
    """
    subtotal = Decimal('0')
    for section in quotation.sections.all():
        calculate_section(section)
        section.save()
        subtotal += section.section_total

    quotation.subtotal = subtotal
    # Example tax calculation logic can go here if needed.
    # Currently assuming tax and additional_charges are explicitly set or calculated elsewhere.
    tax = Decimal(str(quotation.tax)) if quotation.tax else Decimal('0')
    additional = Decimal(str(quotation.additional_charges)) if quotation.additional_charges else Decimal('0')
    
    quotation.total_amount = subtotal + tax + additional
    quotation.save()
    return quotation
