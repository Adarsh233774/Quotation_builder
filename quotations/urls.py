from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('quotations/', views.quotation_list, name='quotation_list'),
    path('quotations/create/', views.quotation_create, name='quotation_create'),
    path('quotations/<int:pk>/', views.quotation_detail, name='quotation_detail'),
    path('quotations/<int:pk>/builder/', views.quotation_builder, name='quotation_builder'),
    path('quotations/<int:pk>/complete/', views.quotation_complete, name='quotation_complete'),
    path('quotations/<int:pk>/htmx/add-section/', views.htmx_add_section, name='htmx_add_section'),
    path('quotations/sections/<int:section_id>/htmx/add-item/', views.htmx_add_item, name='htmx_add_item'),
    path('quotations/items/<int:item_id>/htmx/update/', views.htmx_update_item, name='htmx_update_item'),
]
