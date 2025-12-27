from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = [
            'id', 
            'name', 
            'description', 
            'image',           
            'document',        
            'image_url',       
            'document_url',    
            'created_at', 
            'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_document_url(self, obj):
        if obj.document:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document.url)
        return None