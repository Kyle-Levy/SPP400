from django.urls import path
from . import views

urlpatterns = [
    path('', views.roadmaps_index, name='index'),
    path('create/', views.create_roadmap),
    path('view_roadmap/', views.view_roadmap),
    path('view_roadmap/add/', views.add_to_roadmap),
    path('view_roadmap/remove/', views.remove_selected_pairs),
]
