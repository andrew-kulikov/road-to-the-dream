from django.forms import ModelForm
from django import forms
from .models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'period_count', 'period_val', 'tags', 'task_list', 'repeat_days']
        localized_fields = ['deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'deadline'}),
            'period_val': forms.Select(attrs={'class': 'form-control'}),
            'period_count': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'task_list': forms.Select(attrs={'class': 'form-control'}),
            'repeat_days': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
