from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
]
