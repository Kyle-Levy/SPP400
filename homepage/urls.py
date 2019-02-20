from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in),
    path('logout/', views.log_out),
    #path('code/', views.new_code),
    path('authenticate/', views.authenticator),
    path('homepage/', views.homepage),
]