from django.urls import path
from . import views

urlpatterns = [
    path('procedure/', views.update),
]