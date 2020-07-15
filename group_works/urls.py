'''
Created on Jul 8, 2020

@author: rb18s
'''

"""Defines URL patterns for group_works."""

from django.urls import path

from . import views

app_name = 'group_works'
urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('new_project/', views.new_project, name='new_project'),
    path('new_task/<int:project_id>/', views.new_task, name='new_task'),
    path('edit_project/<int:project_id>/', views.edit_project,
         name='edit_project'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('projects/tasks/<int:task_id>/', views.task, name='task'),
    path('projects/<int:project_id>/', views.project, name='project'),

    ]
