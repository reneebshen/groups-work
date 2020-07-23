'''
Created on Jul 8, 2020

@author: rb18s
'''

"""Defines URL patterns for group_works."""

from django.urls import path

from .views import (
    ProjectListView,
    TaskListView,
    TaskDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskCreateView,
    TaskEditView,
    TaskDeleteView,
    )
from . import views

app_name = 'group_works'
urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/new', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:project_pk>/', TaskListView.as_view(),
         name='task-list'),
    path('projects/<int:project_pk>/update',
        ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:project_pk>/task/new',
         TaskCreateView.as_view(), name='task-create'),
    path('task/<int:task_pk>/',
         TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:task_pk>/update',
         TaskEditView.as_view(), name='task-update'),
    path('projects/<int:project_pk>/delete/',
         ProjectDeleteView.as_view(), name='project-delete'),
    path('task/<int:task_pk>/delete/',
         TaskDeleteView.as_view(), name='task-delete'),
    path('about/', views.about, name='about')

    ]
