from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Setup Router
router = DefaultRouter()
# PENTING: Gunakan string kosong r'' agar endpoint menjadi /api/items/ 
# (sesuai prefix di myproject/urls.py)
router.register(r'', views.ItemViewSet, basename='item')

urlpatterns = [
    # 1. API URLs (Prioritas Utama)
    path('', include(router.urls)),

    # 2. Halaman HTML Legacy (Django Template)
    # Kita pindahkan ke prefix 'html/' agar tidak konflik dengan API JSON
    path('html/home/', views.index, name='index'),
    path('html/list/', views.item_list, name='item_list'),
    path('html/create/', views.item_create, name='item_create'),
    path('html/update/<int:pk>/', views.item_update, name='item_update'),
    path('html/delete/<int:pk>/', views.item_delete, name='item_delete'),
]