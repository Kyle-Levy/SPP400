from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.new_patient),
    path('profile/', views.profile),
]