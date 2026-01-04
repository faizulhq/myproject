from rest_framework import viewsets, permissions, filters, pagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    pagination_class = StandardResultsSetPagination
    
    # Fitur Search & Sorting
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description'] 
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at'] # Default urutan: Terbaru

    def get_permissions(self):
        """
        Mengatur permission secara dinamis agar halaman depan tidak Error 401.
        """
        if self.action in ['list', 'retrieve']:
            # Melihat daftar item & detail item BOLEH PUBLIK (Tanpa Login)
            return [AllowAny()]
        
        # Membuat, Mengedit, Menghapus WAJIB LOGIN
        # Ditambah permission custom untuk memastikan hanya pemilik yang bisa edit
        return [IsAuthenticated(), IsOwnerOrAdminOrPublicReadOnly()]

    def get_queryset(self):
        """
        Mengatur data yang ditampilkan berdasarkan user & scope.
        """
        user = self.request.user
        queryset = Item.objects.all()

        # Ambil parameter scope dari URL
        scope = self.request.query_params.get('scope')

        # 1. Logic Tab 'Milik Saya' (?scope=my)
        if scope == 'my':
            # Jika user belum login (Anonymous) tapi paksa akses ?scope=my,
            # kembalikan list kosong agar tidak error.
            if user.is_anonymous:
                return queryset.none()
            # Tampilkan semua item (Public + Draft) milik user tersebut
            return queryset.filter(owner=user)

        # 2. Logic Default / Tab 'Publik'
        # HANYA tampilkan item dengan status 'public'.
        # Berlaku untuk semua user (termasuk admin) agar tampilan konsisten.
        return queryset.filter(status='public')

    def perform_create(self, serializer):
        # Otomatis set owner ke user yang sedang login saat create
        serializer.save(owner=self.request.user)

# --- Legacy Views (Django Template Biasa) ---
# Kode ini dibiarkan untuk menjaga kompatibilitas URL lama (jika ada)

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