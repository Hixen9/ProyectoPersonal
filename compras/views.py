from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from pedidos.models import EstadoPedido
from carro.models import LineaPedido
from tienda.models import Producto
# Create your views here.

@login_required
def mis_compras(request):
    pedidos_estado = EstadoPedido.objects.filter(username=request.user, pedido__isnull=False)
    return render(request, "compras/mis_compras.html", {"pedidos_estado": pedidos_estado})

@login_required
def detalle_pedido(request, pedido_id):
    # 1) Busca el registro de estado por pedido y usuario
    pedido = get_object_or_404(
        EstadoPedido,
        pedido=pedido_id,
        username=request.user
    )

    # 2) Trae las líneas de pedido
    lineas_raw = LineaPedido.objects.filter(pedido=pedido.pedido)

    # 3) Cargar productos y calcular totales
    lineas = []
    subtotal = 0

    for item in lineas_raw:
        try:
            producto_obj = Producto.objects.get(nombre=item.producto)
            precio_unitario = producto_obj.precio
        except Producto.DoesNotExist:
            precio_unitario = 0

        total_linea = precio_unitario * item.cantidad
        subtotal += total_linea

        lineas.append({
            'producto': producto_obj,
            'cantidad': item.cantidad,
            'precio': precio_unitario,
            'total': total_linea
        })

    # 4) Definir costo de envío (puedes ajustarlo como quieras)
    costo_envio = 0  # Ejemplo: fijo
    total = subtotal + costo_envio

    # 5) Estados de seguimiento
    estados = ['pedido confirmado', 'en recoleccion', 'en ruta', 'entregado']
    if pedido.entregado:
        estado_index = 3
    elif pedido.proceso_envio:
        estado_index = 2
    elif pedido.proceso_recoleccion:
        estado_index = 1
    elif pedido.pedido_confirmado:
        estado_index = 0
    else:
        estado_index = 0

    # 6) Enviar a plantilla
    return render(request, "compras/detalle_pedido.html", {
        'pedido': pedido,
        'lineas': lineas,
        'estados': estados,
        'estado_index': estado_index,
        'subtotal': subtotal,
        'costo_envio': costo_envio,
        'total': total,
    })
