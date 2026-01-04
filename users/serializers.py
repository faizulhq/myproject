from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password tidak cocok."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role', 'user')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # PERBAIKAN: Tambahkan validasi avatar
    avatar = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'website']
        read_only_fields = ['id', 'user']
    
    def validate_avatar(self, value):
        """
        Validasi file avatar
        """
        if value:
            # Cek ukuran file (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Ukuran file maksimal 5MB")
            
            # Cek tipe file
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("File harus berupa gambar")
        
        return value
    
    def update(self, instance, validated_data):
        """
        Override update untuk handle file upload dengan benar
        """
        # Update avatar jika ada
        if 'avatar' in validated_data:
            avatar = validated_data.get('avatar')
            if avatar is None:
                # Hapus avatar lama jika ada
                if instance.avatar:
                    instance.avatar.delete(save=False)
                instance.avatar = None
            else:
                # Hapus avatar lama sebelum upload yang baru
                if instance.avatar:
                    instance.avatar.delete(save=False)
                instance.avatar = avatar
        
        # Update website jika ada
        if 'website' in validated_data:
            instance.website = validated_data.get('website')
        
        instance.save()
        return instance