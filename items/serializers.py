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
        # Set required False agar tidak error jika field kosong
        extra_kwargs = {
            'image': {'required': False},
            'document': {'required': False}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # --- PERBAIKAN: Gunakan try-except untuk mencegah Error 500 ---
        
        # Handle Image
        if instance.image:
            try:
                # Coba ambil URL asli dari Cloudinary
                representation['image'] = instance.image.url
            except AttributeError:
                # Jika error (misal masih berupa string path), kembalikan string-nya saja
                representation['image'] = str(instance.image)

        # Handle Document
        if instance.document:
            try:
                representation['document'] = instance.document.url
            except AttributeError:
                representation['document'] = str(instance.document)
                
        return representation