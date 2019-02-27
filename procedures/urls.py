from django.urls import path
from . import views

urlpatterns = [
    #path('code/', views.new_code),
    path('', views.index, name='index'),
    path('create/', views.new_procedure),
    path('view_procedure/', views.view_procedure),
    path('view_procedure/update/', views.update_procedure),
    path('view_procedure/delete/', views.delete_this_procedure),
]