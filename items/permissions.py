from rest_framework import permissions

class IsOwnerOrAdminOrPublicReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admin: Full Access.
    - Owner: Full Access ke item sendiri.
    - Public: Read Only jika status='public'.
    """
    def has_object_permission(self, request, view, obj):
        # 1. Admin boleh segalanya
        if request.user.is_staff:
            return True

        # 2. Metode Read-Only (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # Boleh baca jika barang sendiri ATAU statusnya public
            return obj.owner == request.user or obj.status == 'public'

        # 3. Metode Write (PUT, DELETE, PATCH)
        # Hanya boleh jika pemilik asli
        return obj.owner == request.user