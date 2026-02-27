from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'created_at', 'updated_at')
    list_filter = ('email_verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'email_verification_token')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Email Verification', {
            'fields': ('email_verified', 'email_verification_token')
        }),
        ('Profile', {
            'fields': ('avatar', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )