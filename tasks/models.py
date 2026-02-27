from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    """Task model for task management"""
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'is_completed']),
        ]

    def __str__(self):
        return self.title

    def mark_complete(self):
        """Mark task as completed"""
        self.is_completed = True
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.is_completed = False
        self.status = 'todo'
        self.completed_at = None
        self.save()

    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.is_completed:
            return self.due_date < timezone.now().date()
        return False

    @property
    def display_status(self):
        """Return human-readable status"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def display_priority(self):
        """Return human-readable priority"""
        return dict(self.PRIORITY_CHOICES).get(self.priority, self.priority)