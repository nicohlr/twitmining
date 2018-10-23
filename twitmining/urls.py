from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('query/', views.query, name='query'),
    path('', views.log_in, name='log_in'),
]
