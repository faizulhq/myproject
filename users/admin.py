from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Inline untuk edit Profile langsung di halaman User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('avatar', 'website')  # Hanya tampilkan field yang relevan

class CustomUserAdmin(UserAdmin):
    # Tambahkan ProfileInline
    inlines = (ProfileInline,)

    # FIELDSETS: Tampilkan 'role' di form edit user
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Tambahan', {
            'fields': ('role',)
        }),
    )
    
    # ADD_FIELDSETS: Saat buat user baru via admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {
            'fields': ('role',)
        }),
    )
    
    # LIST DISPLAY: Tampilkan role di daftar user
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

# Register Model
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)  # Opsional: register Profile terpisah juga