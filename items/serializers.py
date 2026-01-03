from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 
            'name', 
            'description', 
            'image',      
            'document',   
            'created_at', 
            'updated_at'
        ]
        # Set required False agar tidak error saat update tanpa ganti gambar
        extra_kwargs = {
            'image': {'required': False},
            'document': {'required': False}
        }
    
    # Gunakan ini untuk memastikan outputnya tetap Full URL
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = instance.image.url
        if instance.document:
            representation['document'] = instance.document.url
        return representation