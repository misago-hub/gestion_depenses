from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    # champs affichés dans admin
    list_display = ('id', 'email', 'nom', 'role', 'statut', 'is_staff', 'is_active')
    list_filter = ('role', 'statut', 'is_staff', 'is_active')

    ordering = ('email',)  # 🔥 IMPORTANT (plus username)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Infos personnelles', {'fields': ('nom', 'role', 'statut')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )


admin.site.register(User, CustomUserAdmin)
