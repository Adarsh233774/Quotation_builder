from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Quotation, QuotationSection, QuotationItem
from .services.calculation import calculate_item, calculate_section, calculate_quotation
from projects.models import Project

def dashboard(request):
    quotations = Quotation.objects.all().order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {'quotations': quotations})

def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-created_at')
    return render(request, 'quotations/list.html', {'quotations': quotations})

def quotation_create(request):
    if request.method == 'POST':
        # Simple create logic for demonstration
        project_id = request.POST.get('project_id')
        q_num = request.POST.get('quotation_number')
        date = request.POST.get('date')
        
        project = get_object_or_404(Project, id=project_id)
        q = Quotation.objects.create(project=project, quotation_number=q_num, date=date)
        return redirect('quotation_builder', pk=q.pk)
    
    projects = Project.objects.all()
    return render(request, 'quotations/create.html', {'projects': projects})

def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'quotations/detail.html', {'quotation': quotation})

def quotation_builder(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'quotations/builder.html', {'quotation': quotation})

def quotation_complete(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == 'POST':
        quotation.status = 'APPROVED'
        quotation.save()
    return redirect('quotation_builder', pk=pk)

def create_new_version_if_needed(quotation):
    if quotation.status in ['APPROVED', 'SENT', 'ACCEPTED', 'COMPLETED']:
        import json
        from django.core import serializers
        
        # Create snapshot data
        # Just a basic dump of items and sections for now, or just the whole quotation
        qs_json = serializers.serialize('json', [quotation])
        from .models import QuotationVersion
        QuotationVersion.objects.create(
            original_quotation=quotation,
            version_number=quotation.version,
            snapshot_data=json.loads(qs_json)
        )
        
        quotation.version += 1
        quotation.status = 'DRAFT'
        base_num = quotation.quotation_number.split('-v')[0]
        quotation.quotation_number = f"{base_num}-v{quotation.version}"
        quotation.save()

def htmx_add_section(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == 'POST':
        create_new_version_if_needed(quotation)
        name = request.POST.get('name', 'New Section')
        section = QuotationSection.objects.create(quotation=quotation, name=name)
        # return the HTML snippet for the new section
        return render(request, 'quotations/partials/section.html', {'section': section})
    return HttpResponse(status=400)

def htmx_add_item(request, section_id):
    section = get_object_or_404(QuotationSection, pk=section_id)
    if request.method == 'POST':
        create_new_version_if_needed(section.quotation)
        item = QuotationItem.objects.create(section=section, description='New Item')
        return render(request, 'quotations/partials/item_row.html', {'item': item})
    return HttpResponse(status=400)

def htmx_update_item(request, item_id):
    item = get_object_or_404(QuotationItem, pk=item_id)
    if request.method == 'POST':
        try:
            create_new_version_if_needed(item.section.quotation)
            print("DEBUG POST:", request.POST, "TRIGGER:", request.headers.get('HX-Trigger-Name'))
            item.description = request.POST.get('description', item.description)
            item.calculation_type = request.POST.get('calculation_type', item.calculation_type)
            
            # safely get decimals
            def update_decimal(field_name, default=None):
                if field_name in request.POST:
                    val = request.POST.get(field_name)
                    if val and val.strip():
                        # Clean string of any commas or symbols if needed
                        val = str(val).replace(',', '')
                        setattr(item, field_name, val)
                    else:
                        setattr(item, field_name, default)

            update_decimal('length')
            update_decimal('width')
            update_decimal('quantity', 1)
            update_decimal('rate', 0)
            update_decimal('amount', 0)
            
            trigger_name = request.headers.get('HX-Trigger-Name')
            if trigger_name == 'amount':
                item._manual_amount_override = True
                item.calculation_type = 'FIXED'  # Automatically switch to Fixed if they manually override amount
            
            # Calculate amount using service
            calculate_item(item)
            item.save()
            
            # Trigger recalculation up the chain
            calculate_section(item.section)
            item.section.save()
            
            calculate_quotation(item.section.quotation)
            
            return render(request, 'quotations/partials/item_row.html', {'item': item})
        except Exception as e:
            import traceback
            print("ERROR IN htmx_update_item:", e)
            traceback.print_exc()
            return HttpResponse(status=500)
    return HttpResponse(status=400)
