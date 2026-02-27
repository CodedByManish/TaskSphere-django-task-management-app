from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'due_date', 'is_completed', 'created_at')
    list_filter = ('status', 'priority', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    fieldsets = (
        ('Task Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Details', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Completion', {
            'fields': ('is_completed', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Automatically set user to current user if not set"""
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)