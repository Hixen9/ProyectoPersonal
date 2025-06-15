from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from pedidos.models import EstadoPedido
from carro.models import LineaPedido

@login_required
def mis_compras(request):
    pedidos_estado = EstadoPedido.objects.filter(username=request.user)
    return render(request, "compras/mis_compras.html", {
        "pedidos_estado": pedidos_estado
    })

@login_required
def detalle_pedido(request, pedido_id):
    # 1) Busca el registro de estado por el campo 'pedido' y el usuario
    pedido = get_object_or_404(
        EstadoPedido,
        pedido=pedido_id,
        username=request.user
    )

    # 2) Todas las líneas de ese pedido (filtro por el mismo campo 'pedido')
    lineas = LineaPedido.objects.filter(pedido=pedido_id)

    # 3) Lista de nombres de estado para la barra de progreso
    estados = ['pedido confirmado', 'en transito', 'en ruta', 'entregado']

    # 4) Determina en qué índice estamos según los booleanos
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

    # 5) Cálculo de totales (por ahora puedes usar precio=0 si no lo tienes aún)
    subtotal = sum(getattr(item, 'cantidad', 0) * 0 for item in lineas)
    costo_envio = getattr(pedido, 'costo_envio', 0)
    total = subtotal + costo_envio

    # 6) Renderiza la plantilla con toda la info
    return render(request, "compras/detalle_pedido.html", {
        'pedido': pedido,
        'lineas': lineas,
        'estados': estados,
        'estado_index': estado_index,
        'subtotal': subtotal,
        'costo_envio': costo_envio,
        'total': total,
    })