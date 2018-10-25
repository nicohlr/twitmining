from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_in, name='log_in'),
    path('home/', views.home, name='home'),
    path('query/', views.query, name='query'),
    path('logout/', views.log_out, name='log_out'),
    path('sign_up/', views.sign_up, name='signup')
]
