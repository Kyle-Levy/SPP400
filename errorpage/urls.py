from django.urls import path
from . import views

urlpatterns = [
    #path('code/', views.new_code),
    path('', views.error),
]