from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, index  

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', index, name='index'),  
    path('', include(router.urls)),
]