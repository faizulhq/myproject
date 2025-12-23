from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    # Halaman Utama
    path('', views.index, name='index'),
    
    # Halaman CRUD Baru
    path('list/', views.item_list, name='item_list'),
    path('create/', views.item_create, name='item_create'),
    path('update/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),

    # API URLs
    path('', include(router.urls)),
]
