"""
Tasks App Views

This module contains all view functions for task management including:
- Task CRUD operations
- Task filtering and search
- Task completion tracking
- API endpoints for AJAX requests
- Dashboard with statistics
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Task
from .forms import TaskForm, TaskSearchForm
from datetime import datetime
from django.http import HttpResponse
import json


def home(request):
    """
    Home page view
    Displays landing page for unauthenticated users
    Redirects authenticated users to dashboard
    """
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')
    return render(request, 'tasks/home.html')


@login_required(login_url='accounts:login')
def dashboard(request):
    """
    Main dashboard view
    Displays user's tasks with statistics and filtering options
    
    Features:
    - Task statistics (total, completed, pending, overdue)
    - Task organization by status
    - Search and filter functionality
    - Priority-based organization
    """
    user = request.user
    
    # Get all user tasks
    tasks = Task.objects.filter(user=user)
    
    # Apply search and filter
    form = TaskSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        status_filter = form.cleaned_data.get('status')
        priority_filter = form.cleaned_data.get('priority')
        
        if search_query:
            tasks = tasks.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)
    
    # Calculate statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = tasks.filter(is_completed=False).count()
    overdue_tasks = tasks.filter(
        due_date__lt=timezone.now().date(),
        is_completed=False
    ).count()
    
    # Organize tasks by status
    todo_tasks = tasks.filter(status='todo')
    in_progress_tasks = tasks.filter(status='in_progress')
    completed = tasks.filter(status='completed')
    
    # Get high priority tasks
    high_priority_tasks = tasks.filter(priority='high', is_completed=False)[:5]
    
    # Calculate completion percentage
    completion_percentage = (
        (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    )
    
    context = {
        'form': form,
        'all_tasks': tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed,
        'high_priority_tasks': high_priority_tasks,
        'stats': {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'overdue': overdue_tasks,
            'completion_percentage': int(completion_percentage),
        }
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def create_task(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully! ✓')
            return redirect('tasks:dashboard')
        else:
            messages.error(request, 'Error creating task. Please check the form.')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create New Task',
        'button_text': 'Create Task'
    })


@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def edit_task(request, pk):
    """
    Edit an existing task
    
    GET: Display task edit form with current data
    POST: Process form and update task
    
    Args:
        pk (int): Primary key of the task to edit
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully! ✓')
            return redirect('tasks:task_detail', pk=pk)
        else:
            messages.error(request, 'Error updating task. Please check the form.')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task',
        'task': task,
        'button_text': 'Update Task'
    })


@login_required(login_url='accounts:login')
@require_http_methods(["GET"])
def task_detail(request, pk):
    """
    View task details
    
    Displays full task information including description, due date,
    priority, status, and action buttons
    
    Args:
        pk (int): Primary key of the task to view
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Get related tasks (same status or priority)
    related_tasks = Task.objects.filter(
        user=request.user,
        status=task.status
    ).exclude(pk=pk)[:5]
    
    context = {
        'task': task,
        'related_tasks': related_tasks,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required(login_url='accounts:login')
@require_POST
def delete_task(request, pk):
    """
    Delete a task
    
    Removes the task from the database after confirmation
    
    Args:
        pk (int): Primary key of the task to delete
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task_title = task.title
    task.delete()
    messages.success(request, f'Task "{task_title}" deleted successfully! ✓')
    return redirect('tasks:dashboard')


@login_required(login_url='accounts:login')
@require_POST
def toggle_task_complete(request, pk):
    """
    Toggle task completion status
    
    Marks task as complete/incomplete. Supports both HTML forms and AJAX requests.
    
    Args:
        pk (int): Primary key of the task to toggle
        
    Returns:
        JSON response for AJAX requests
        Redirect response for form submissions
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if task.is_completed:
            task.mark_incomplete()
            message = 'Task marked as incomplete'
            status = 'incomplete'
        else:
            task.mark_complete()
            message = 'Task completed successfully!'
            status = 'complete'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'is_completed': task.is_completed,
            'status': task.status,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        })
    else:
        # Standard form submission
        if task.is_completed:
            task.mark_incomplete()
            messages.success(request, 'Task marked as incomplete')
        else:
            task.mark_complete()
            messages.success(request, 'Task marked as complete!')
        return redirect('tasks:dashboard')


# ============================================
# API Endpoints (JSON responses)
# ============================================

@login_required(login_url='accounts:login')
def api_task_list(request):
    """
    API endpoint to get list of user's tasks as JSON
    
    Query Parameters:
        - search: Search term for title/description
        - status: Filter by status
        - priority: Filter by priority
        - limit: Number of tasks to return (default: 20)
    
    Returns:
        JSON response with task list
    """
    tasks = Task.objects.filter(user=request.user)
    
    # Apply filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    limit = int(request.GET.get('limit', 20))
    
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    if status:
        tasks = tasks.filter(status=status)
    
    if priority:
        tasks = tasks.filter(priority=priority)
    
    # Limit results
    tasks = tasks[:limit]
    
    # Serialize data
    data = {
        'count': tasks.count(),
        'tasks': [
            {
                'id': task.pk,
                'title': task.title,
                'status': task.status,
                'priority': task.priority,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'is_completed': task.is_completed,
                'created_at': task.created_at.isoformat(),
            }
            for task in tasks
        ]
    }
    
    return JsonResponse(data)


@login_required(login_url='accounts:login')
def api_task_detail(request, pk):
    """
    API endpoint to get single task details as JSON
    
    Args:
        pk (int): Primary key of the task
    
    Returns:
        JSON response with task details
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    data = {
        'id': task.pk,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'is_completed': task.is_completed,
        'created_at': task.created_at.isoformat(),
        'updated_at': task.updated_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'is_overdue': task.is_overdue(),
    }
    
    return JsonResponse(data)


@login_required(login_url='accounts:login')
@require_POST
def api_task_status(request, pk):
    """
    API endpoint to update task status
    
    Expects JSON payload:
    {
        'status': 'todo|in_progress|completed'
    }
    
    Args:
        pk (int): Primary key of the task
    
    Returns:
        JSON response with updated task data
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Status updated successfully',
                'status': task.status,
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid status',
            }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON',
        }, status=400)


@login_required(login_url='accounts:login')
def api_statistics(request):
    """
    API endpoint to get task statistics as JSON
    
    Returns:
        JSON response with task statistics including:
        - Total tasks
        - Completed tasks
        - Pending tasks
        - Overdue tasks
        - Tasks by status and priority
        - Completion percentage
    """
    tasks = Task.objects.filter(user=request.user)
    
    total = tasks.count()
    completed = tasks.filter(is_completed=True).count()
    pending = tasks.filter(is_completed=False).count()
    overdue = tasks.filter(
        due_date__lt=timezone.now().date(),
        is_completed=False
    ).count()
    
    # Count by status
    by_status = {
        status: tasks.filter(status=status).count()
        for status, _ in Task.STATUS_CHOICES
    }
    
    # Count by priority
    by_priority = {
        priority: tasks.filter(priority=priority).count()
        for priority, _ in Task.PRIORITY_CHOICES
    }
    
    completion_percentage = (
        (completed / total * 100) if total > 0 else 0
    )
    
    data = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'completion_percentage': round(completion_percentage, 2),
        'by_status': by_status,
        'by_priority': by_priority,
    }
    
    return JsonResponse(data)


# ============================================
# Error Handlers
# ============================================
def handler_404(request, exception):
    try:
        return render(request, 'errors/404.html', status=404)
    except:
        return HttpResponse("<h1>404 - Page Not Found</h1><p>The TaskSphere resource you requested was not found.</p>", status=404)

def handler_500(request):
    try:
        return render(request, 'errors/500.html', status=500)
    except:
        return HttpResponse("<h1>500 - Server Error</h1><p>Something went wrong internally.</p>", status=500)