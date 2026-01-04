from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    # Menampilkan username pemilik item (Read Only)
    owner_username = serializers.ReadOnlyField(source='owner.username')
    is_my_item = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'image', 'document', 'status', 'owner', 'owner_username', 'is_my_item', 'created_at']
        read_only_fields = ['owner', 'created_at'] # Owner otomatis diisi backend

    def get_is_my_item(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.owner == request.user
        return False