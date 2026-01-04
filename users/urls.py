from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, ProfileView, ProfileViewSet

# Router untuk ProfileViewSet
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='user-profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ProfileView.as_view(), name='me'), # Endpoint user detail dasar
    
    # Include Router (endpoint: /api/auth/profiles/)
    path('', include(router.urls)), 
]