from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('tweets/', views.tweets, name='tweets'),
    path('tweets/empty/', views.empty_database, name='empty')
]