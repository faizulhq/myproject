from rest_framework import generics, permissions, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from .models import Profile

User = get_user_model()

# CUSTOM JWT SERIALIZER: Tambahkan user data di response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Tambahkan user data ke response
        data['user'] = UserSerializer(self.user).data
        
        return data

# CUSTOM LOGIN VIEW
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        """
        Lazy Creation + Return QuerySet yang benar
        """
        user = self.request.user
        
        # Cek apakah profile sudah ada
        profile_exists = Profile.objects.filter(user=user).exists()
        
        if not profile_exists:
            # Buat profile baru jika belum ada
            print(f"🔧 Creating profile for user: {user.username}")
            Profile.objects.create(user=user)
        
        # Return QuerySet (bukan single object!)
        return Profile.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        """
        Override list() untuk memastikan return array
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        print(f"📋 List profiles for {request.user.username}: {len(serializer.data)} found")
        
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve() untuk validasi ownership
        """
        instance = self.get_object()
        
        # Security check: hanya boleh akses profile sendiri
        if instance.user != request.user:
            return Response(
                {"detail": "You don't have permission to access this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        PERBAIKAN: Handle FormData untuk file upload
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Security check
        if instance.user != request.user:
            return Response(
                {"detail": "You don't have permission to edit this profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        print(f"📝 Updating profile ID {instance.id} for user: {request.user.username}")
        print(f"📦 Content-Type: {request.content_type}")
        print(f"📦 Data keys: {list(request.data.keys())}")
        print(f"📦 Files keys: {list(request.FILES.keys())}")
        
        # Validasi data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            print(f"✅ Profile updated successfully")
            print(f"✅ New avatar URL: {serializer.data.get('avatar')}")
            
            return Response(serializer.data)
        except Exception as e:
            print(f"❌ Validation Error: {str(e)}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        """
        Save update (user otomatis dari request)
        """
        # JANGAN pass user lagi, karena sudah OneToOne field yang read-only
        serializer.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint shortcut: GET /api/auth/profiles/me/
        Return profile user yang sedang login
        """
        profile = self.get_queryset().first()
        
        if not profile:
            return Response(
                {"detail": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)