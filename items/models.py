from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Item(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft (Pribadi)'),
        ('public', 'Publik (Semua Orang)'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items/images/', null=True, blank=True)
    document = models.FileField(upload_to='items/documents/', null=True, blank=True)
    
    # Field Baru
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"