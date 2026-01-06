from rest_framework import viewsets, permissions, filters, pagination, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from django.db import models  
from .models import Item
from .serializers import ItemSerializer
from .permissions import IsOwnerOrAdminOrPublicReadOnly
import traceback

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description'] 
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdminOrPublicReadOnly()]

    # === LOGIKA PERBAIKAN (FIX ERROR 404) ===
    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.all()
        scope = self.request.query_params.get('scope')

        # 1. Jika user minta list miliknya sendiri (?scope=my)
        if scope == 'my':
            if user.is_anonymous:
                return queryset.none()
            return queryset.filter(owner=user)
        
        # 2. Jika Detail/Update/Delete (Akses ke satu item spesifik)
        # Izinkan akses jika item itu Public ATAU milik user sendiri (meskipun Draft)
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            if user.is_authenticated:
                # Gunakan Q objects untuk logika OR: Public ATAU Milik Sendiri
                return queryset.filter(models.Q(status='public') | models.Q(owner=user))

        # 3. Default List (Halaman Depan): Hanya item Public
        return queryset.filter(status='public')

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return Response(
                {"detail": "Gagal menyimpan item.", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# --- Legacy Views ---
def index(request): return render(request, 'items/index.html')
def item_list(request): return render(request, 'items/item_list.html')
def item_create(request): return render(request, 'items/item_form.html')
def item_update(request, pk): return render(request, 'items/item_form.html')
def item_delete(request, pk): return render(request, 'items/item_confirm_delete.html')
