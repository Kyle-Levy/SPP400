from django.urls import path
from . import views

urlpatterns = [
    #path('code/', views.new_code),
    path('', views.index, name='index'),
    path('create/', views.new_procedure),
]