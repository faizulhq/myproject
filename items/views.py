from rest_framework import viewsets, permissions, filters, pagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from .models import Item
from .serializers import ItemSerializer
from .permissions import IsOwnerOrAdminOrPublicReadOnly

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrPublicReadOnly]
    pagination_class = StandardResultsSetPagination
    
    # Fitur Search & Sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description'] 
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at'] # Default urutan: Terbaru

    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.all()

        # Ambil parameter scope dari URL (frontend mengirim ?scope=my atau ?scope=public)
        scope = self.request.query_params.get('scope')

        # LOGIKA PERBAIKAN:
        # Aturan ini berlaku mutlak untuk Admin maupun User biasa.
        
        if scope == 'my':
            # Tab 'Milik Saya': Tampilkan SEMUA item milik user yang login (Draft + Public)
            return queryset.filter(owner=user)

        # Tab 'Publik' (atau default jika tidak ada scope):
        # HANYA tampilkan item dengan status 'public'.
        # Admin tidak boleh melihat 'draft' orang lain di tab ini agar UI tetap rapi.
        return queryset.filter(status='public')

    def perform_create(self, serializer):
        # Otomatis set owner ke user yang sedang login
        serializer.save(owner=self.request.user)

# --- Legacy Views (Django Template Biasa) ---
# Kode ini tetap dibiarkan agar tidak error jika ada sisa import URL lama

def index(request):
    return render(request, 'items/index.html')

def item_list(request):
    return render(request, 'items/item_list.html')

def item_create(request):
    return render(request, 'items/item_form.html')

def item_update(request, pk):
    return render(request, 'items/item_form.html')

def item_delete(request, pk):
    return render(request, 'items/item_confirm_delete.html')