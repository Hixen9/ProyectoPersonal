from django.urls import path
from .views import VRegistro,cerrar_sesion,loguear

urlpatterns = [
    path('',VRegistro.as_view(),name="Autenticacion"),
    path('cerrar_sesion',cerrar_sesion,name="cerrar_sesion"),
    path('logear',loguear,name="logear"),
]