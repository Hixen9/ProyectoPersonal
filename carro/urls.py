from django.urls import path
from . import views

app_name="carro"

urlpatterns = [
    path("agregar/<int:producto_id>/",views.agregar_producto, name="agregar"),
    path("eliminar/<int:producto_id>/",views.eliminar_producto, name="eliminar"),
    path("restar/<int:producto_id>/",views.restar_producto, name="restar"),
    path("limpar/",views.limpiar_carro, name="limpar")
]