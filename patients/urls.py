from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.new_patient),
    path('profile/', views.profile),
    path('profile/update/', views.update),
    path('profile/delete/', views.delete),
    path('profile/procedures/', views.procedures)
]
