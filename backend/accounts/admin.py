from django.contrib import admin
from .models import User, DeaneryAccount, StaffAccount
from django.db import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import Textarea


class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ('email', 'first_name',)
    ordering = ['email']
    list_filter = ('email', 'first_name', 'is_active', 'is_staff')
    list_display = ('email', 'is_active', 'is_staff', 'is_dean')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_dean', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_dean')}
         ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(DeaneryAccount)
admin.site.register(StaffAccount)