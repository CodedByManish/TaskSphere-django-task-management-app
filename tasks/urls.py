"""
Tasks App URL Configuration

This module defines URL patterns for task management operations including
CRUD operations, task completion toggling, and the dashboard.

URL Patterns:
- / - Home page
- dashboard/ - Main task dashboard
- create/ - Create new task
- task/<id>/ - View task details
- task/<id>/edit/ - Edit task
- task/<id>/delete/ - Delete task
- task/<id>/toggle/ - Toggle task completion status
"""

from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Task CRUD Operations
    path('create/', views.create_task, name='create_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    
    # Task Status Management
    path('task/<int:pk>/toggle/', views.toggle_task_complete, name='toggle_task'),
    
    # API Endpoints (JSON responses)
    path('api/tasks/', views.api_task_list, name='api_task_list'),
    path('api/task/<int:pk>/', views.api_task_detail, name='api_task_detail'),
    path('api/task/<int:pk>/status/', views.api_task_status, name='api_task_status'),
    path('api/statistics/', views.api_statistics, name='api_statistics'),
]