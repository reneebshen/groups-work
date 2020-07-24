from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

# Create your models here.


class Project(models.Model):
    """A project the user is collaborating on."""
    title = models.CharField(max_length=100)
    last_edit = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()  # use a DateInput widget
    description = models.TextField(default='No Description.')
    complete = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # collaborators =

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    def get_absolute_url(self):
        return reverse('group_works:task-list', kwargs={'project_pk':self.pk})


class Task(models.Model):
    """A task to be completed for a project."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    last_edit = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    complete = models.BooleanField(default=False)
    description = models.TextField(default='No Description.')

    # collaborators =

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    def get_absolute_url(self):
        return reverse('group_works:task-detail', kwargs={'task_pk':self.pk})

