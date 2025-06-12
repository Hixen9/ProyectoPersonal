from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pedidos.models import EstadoPedido
from carro.models import LineaPedido
# Create your views here.

@login_required
def mis_compras(request):
    pedidos_estado = EstadoPedido.objects.filter(username=request.user)
    return render(request, "compras/mis_compras.html", {"pedidos_estado": pedidos_estado})

@login_required
def detalle_pedido(request, pedido_id):
    lineas = LineaPedido.objects.filter(pedido=pedido_id)
    return render(request, "compras/detalle_pedido.html", {"lineas": lineas, "pedido_id": pedido_id})
