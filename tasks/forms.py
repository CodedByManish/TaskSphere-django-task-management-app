from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Task description (optional)',
                'rows': 4,
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Due date',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class TaskSearchForm(forms.Form):
    """Form for searching and filtering tasks"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Status')] + Task.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    priority = forms.ChoiceField(
        required=False,
        choices=[('', 'All Priorities')] + Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )