from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    # Force absolute URL untuk image dan document
    image = serializers.SerializerMethodField()
    document = serializers.SerializerMethodField()
    
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
    
    def get_image(self, obj):
        if obj.image:
            # CloudinaryField.url sudah return full URL
            return str(obj.image.url) if hasattr(obj.image, 'url') else str(obj.image)
        return None
    
    def get_document(self, obj):
        if obj.document:
            return str(obj.document.url) if hasattr(obj.document, 'url') else str(obj.document)
        return None