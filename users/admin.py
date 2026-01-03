from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Menambahkan field 'role' dan 'avatar' ke fieldsets (Edit Form)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Info', {'fields': ('role', 'avatar')}),
    )
    # Menambahkan ke add_fieldsets (Create Form)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Info', {'fields': ('role', 'avatar')}),
    )
    # Menampilkan kolom role di list user
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']

admin.site.register(User, CustomUserAdmin)