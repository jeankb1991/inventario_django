
from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel, name='painel'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/add/', views.category_create, name='category-add'),
    path('categories/<int:pk>/edit/', views.category_update, name='category-edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),

    path('items/', views.item_list, name='item-list'),
    path('items/add/', views.item_create, name='item-add'),
    path('items/<int:pk>/', views.item_detail, name='item-detail'),
    path('items/<int:pk>/edit/', views.item_update, name='item-edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item-delete'),

    path('reports/items/pdf/', views.items_pdf, name='items-pdf'),
]
