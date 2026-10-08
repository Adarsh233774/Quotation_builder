from django.shortcuts import render, redirect
from .models import Project
from clients.models import Client

# Create your views here.
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        client_id = request.POST.get('client_id')
        location = request.POST.get('location')
        project_type = request.POST.get('project_type')
        reference = request.POST.get('reference')
        
        client = Client.objects.get(id=client_id)
        Project.objects.create(
            name=name,
            client=client,
            location=location,
            project_type=project_type,
            reference=reference
        )
        return redirect('quotation_create')
    
    clients = Client.objects.all()
    return render(request, 'projects/create.html', {'clients': clients})
