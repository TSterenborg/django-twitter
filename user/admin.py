from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'display_name', 'password', 'last_login', 'created_at', 'is_active', 'is_staff', 'is_admin', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('display_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'username', 'display_name', 'password1', 'password2', 'is_staff', 'is_active')}),
    )
    search_fields = ('email', 'username', 'display_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
