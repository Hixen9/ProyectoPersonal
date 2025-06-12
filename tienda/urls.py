from django.urls import path
from tienda import views

urlpatterns = [
    path('',views.tienda,name="Tienda"),
    path('tienda/producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
]
