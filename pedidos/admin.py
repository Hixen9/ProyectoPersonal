from django.contrib import admin
from .models import Pedido,Recibo,Paqueteria,EstadoPedido

admin.site.register(Pedido)
admin.site.register(Recibo)
admin.site.register(Paqueteria)
admin.site.register(EstadoPedido)
# Register your models here.

