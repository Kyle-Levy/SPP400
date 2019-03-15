from django.urls import path
from . import views


urlpatterns = [
    path('', views.add_model, name='index'),
    path('create/', views.create_roadmap),
]
