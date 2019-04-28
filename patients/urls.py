from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.new_patient),
    path('profile/', views.profile),
    path('profile/update/', views.update),
    path('profile/delete/', views.delete),
    path('profile/procedures/', views.procedures),
    path('profile/procedures/add_roadmap/', views.add_roadmap),
    path('profile/procedures/add_procedure/', views.add_procedure),
    path('profile/procedures/remove/', views.remove_pairs_from_patient),
    path('profile/flag/', views.flag_patient),
    path('profile/unflag/', views.unflag_patient),
    path('profile/check_procedures/', views.checkbox_submission),
]
