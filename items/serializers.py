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

