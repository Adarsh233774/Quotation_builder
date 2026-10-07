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

def htmx_add_section(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', 'New Section')
        section = QuotationSection.objects.create(quotation=quotation, name=name)
        # return the HTML snippet for the new section
        return render(request, 'quotations/partials/section.html', {'section': section})
    return HttpResponse(status=400)

def htmx_add_item(request, section_id):
    section = get_object_or_404(QuotationSection, pk=section_id)
    if request.method == 'POST':
        item = QuotationItem.objects.create(section=section, description='New Item')
        return render(request, 'quotations/partials/item_row.html', {'item': item})
    return HttpResponse(status=400)

def htmx_update_item(request, item_id):
    item = get_object_or_404(QuotationItem, pk=item_id)
    if request.method == 'POST':
        item.description = request.POST.get('description', item.description)
        item.calculation_type = request.POST.get('calculation_type', item.calculation_type)
        
        # safely get decimals
        def get_decimal(field_name, default=None):
            val = request.POST.get(field_name)
            if val and val.strip():
                return val
            return default

        item.length = get_decimal('length')
        item.width = get_decimal('width')
        item.quantity = get_decimal('quantity', 1)
        item.rate = get_decimal('rate', 0)
        
        # Calculate amount using service
        calculate_item(item)
        item.save()
        
        # Trigger recalculation up the chain
        calculate_section(item.section)
        item.section.save()
        
        calculate_quotation(item.section.quotation)
        
        # Re-render the single item row or the section totals
        # In a real app we might return OOB (Out of Band) updates to update totals
        return render(request, 'quotations/partials/item_row.html', {'item': item})
    return HttpResponse(status=400)
