from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Agar bisa edit Profile (Avatar/Website) di dalam halaman User
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    # Tambahkan Inline
    inlines = (ProfileInline,)

    # FIELDSETS: Tampilkan 'role' saja, JANGAN 'avatar' (karena ada di inline)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role',)}), 
    )
    
    # ADD_FIELDSETS: Saat buat user baru
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {'fields': ('role',)}),
    )
    
    # LIST DISPLAY: Kembalikan 'role'
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']

admin.site.register(User, CustomUserAdmin)
# Opsional: Register Profile terpisah juga
admin.site.register(Profile)