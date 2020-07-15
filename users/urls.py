'''
Created on Jul 10, 2020

@author: rb18s
'''

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    ]
