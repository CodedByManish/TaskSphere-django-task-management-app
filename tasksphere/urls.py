"""
TaskSphere Main URL Configuration

This module defines the primary URL routing for the TaskSphere application.
It includes patterns for the admin interface, user accounts, and task management.

URL Patterns:
- /admin/ - Django admin interface
- /accounts/ - User authentication and profile management
- /tasks/ - Task management views
- / - Home and dashboard views
"""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Main URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls', namespace='tasks')),  # <-- check this
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # Do NOT include tasks.urls again with namespace='tasks'
    path('', lambda request: redirect('tasks:home')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers (optional)
handler404 = 'tasks.views.handler_404'
handler500 = 'tasks.views.handler_500'