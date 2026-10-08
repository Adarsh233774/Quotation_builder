from django.shortcuts import render, redirect
from .models import Client

# Create your views here.
def client_list(request):
    # Prefetch projects and their quotations to avoid N+1 queries
    clients = Client.objects.prefetch_related('projects__quotations').all()
    return render(request, 'clients/list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        company = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        Client.objects.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address=address
        )
        return redirect('project_create')
    
    return render(request, 'clients/create.html')
