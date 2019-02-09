from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-test'),
    path('login/', views.log_in),
]