from rest_framework import viewsets, permissions, filters, pagination, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import render
from .models import Item
from .serializers import ItemSerializer
from .permissions import IsOwnerOrAdminOrPublicReadOnly
import traceback # PENTING: Untuk melihat error asli di log

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    # Parser untuk menangani form-data (Upload Gambar/File)
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrPublicReadOnly]
    pagination_class = StandardResultsSetPagination
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description'] 
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.all()
        scope = self.request.query_params.get('scope')

        if scope == 'my':
            if user.is_anonymous:
                return queryset.none()
            return queryset.filter(owner=user)

        return queryset.filter(status='public')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdminOrPublicReadOnly()]

    # === MODIFIKASI DEBUG: Menangkap Error 500 ===
    def create(self, request, *args, **kwargs):
        """
        Override create untuk menangkap error sistem dan menampilkannya
        """
        try:
            print("📦 [DEBUG] Mencoba create item...")
            print(f"📦 [DEBUG] User: {request.user}")
            print(f"📦 [DEBUG] Data: {request.data}")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("\n❌ [ERROR FATAL] Gagal Create Item:")
            print(f"❌ Type: {type(e)}")
            print(f"❌ Message: {str(e)}")
            traceback.print_exc() # Print error lengkap ke log Railway
            
            # Kembalikan pesan error ke Frontend (JSON) agar tidak cuma 'Server Error'
            return Response(
                {
                    "detail": "Gagal menyimpan item.",
                    "error_type": str(type(e).__name__),
                    "error_message": str(e)
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        # Set owner ke user yang sedang login
        serializer.save(owner=self.request.user)

# --- Legacy Views ---
def index(request): return render(request, 'items/index.html')
def item_list(request): return render(request, 'items/item_list.html')
def item_create(request): return render(request, 'items/item_form.html')
def item_update(request, pk): return render(request, 'items/item_form.html')
def item_delete(request, pk): return render(request, 'items/item_confirm_delete.html')