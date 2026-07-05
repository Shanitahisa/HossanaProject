from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.resortIndex, name='resortIndex'),
    path('resortIndex/', views.resortIndex, name='resortIndex'),
    
    
]
