# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-cancelado/', views.pago_cancelado, name='pago_cancelado'),
]
