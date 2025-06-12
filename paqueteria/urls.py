from django.urls import path
from . import views

urlpatterns = [
    path('paqueteria/login/', views.paqueteria_login, name='paqueteria_login'),
    path('paqueteria/dashboard/', views.paqueteria_dashboard, name='paqueteria_dashboard'),
    path('paqueteria/logout/', views.paqueteria_logout, name='paqueteria_logout'),
]
