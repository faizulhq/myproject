from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from .models import Profile

User = get_user_model()

# Auth Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

# Profile Management ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # PENTING: Tambahkan parser ini agar bisa upload file
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        # Cek apakah profil ada, jika tidak, buatkan (Lazy Creation)
        queryset = Profile.objects.filter(user=self.request.user)
        if not queryset.exists():
            Profile.objects.create(user=self.request.user)
            queryset = Profile.objects.filter(user=self.request.user)
        return queryset

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)