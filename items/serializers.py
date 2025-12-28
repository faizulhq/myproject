from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # Kita hapus image_url dan document_url buatan manual.
        # Field 'image' dan 'document' dari Cloudinary sudah otomatis berupa URL lengkap.
        fields = [
            'id', 
            'name', 
            'description', 
            'image',     # Ini akan otomatis jadi URL (https://res.cloudinary...)
            'document',  # Ini juga otomatis jadi URL
            'created_at', 
            'updated_at'
        ]

