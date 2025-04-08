from django.urls import path
from tienda import views

urlpatterns = [
    path('',views.tienda,name="Tienda"),
]