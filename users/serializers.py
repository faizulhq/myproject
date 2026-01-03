from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'avatar', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'required': False} # Avatar opsional saat register
        }

    def create(self, validated_data):
        # Hash password saat register
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    # Serializer khusus untuk update profil (termasuk avatar)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'avatar']
        read_only_fields = ['role'] # User gabisa ubah role sendiri