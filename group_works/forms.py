'''
Created on Jul 10, 2020

@author: rb18s
'''

from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'due_date', 'description']
        labels = {'title': 'Title', 'due_date': 'Due Date',
                  'description': 'Describe your project:'}
        widgets = {'due_date': forms.DateInput(),
                   'description': forms.Textarea(attrs={'cols': 80})}
        # add a datepicker calender widget


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'description']
        labels = {'title': 'Title', 'due_date': 'Due Date',
                  'description': 'Describe the task:'}
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}
