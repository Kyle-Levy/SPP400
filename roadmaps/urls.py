from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_roadmap),
    path('view_roadmap/', views.view_roadmap),
    path('view_roadmap/add/', views.add_to_roadmap),
]
