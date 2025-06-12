from django.urls import path
from . import views

urlpatterns = [
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('mis-compras/detalle/<str:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]