from django.shortcuts import redirect, render
from carro.carro import Carro
from carro.models import LineaPedido
from django.contrib.auth.models import User
from pedidos.models import Pedido
from tienda.models import Producto
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


from django.contrib.auth.decorators import login_required

@login_required(login_url="/autenticacion/logear")
def procesar_pedido(request):
    username = request.user.username  # usamos el Username como en tu base
    carro = Carro(request)

    # Creamos el pedido principal
    pedido = Pedido.objects.create(user=request.user)

    lineas_pedido = []

    for key, value in carro.carro.items():
        producto = Producto.objects.get(id=key)

        lineas_pedido.append(
            LineaPedido(
                username=username,
                producto=producto.nombre,
                cantidad=value["cantidad"],
                pedido=str(pedido.id),
                
            )
        )

        # Reducir el stock del producto
        producto.cantidad -= value["cantidad"]
        if producto.cantidad <= 0:
            producto.disponibilidad = False
        producto.save()

    LineaPedido.objects.bulk_create(lineas_pedido)

    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_pedido,
        usuario=username,
        email=request.user.email,
    )
    
    messages.success(request, "El pedido ha sido creado correctamente")
    carro.limpiar_carro()
    total = sum(float(item["precio"]) for item in carro.carro.values())
    # Mostrar resumen del pedido
    return render(request, "resumen_pedido.html", {
        "pedido": pedido,
        "lineas": lineas_pedido,
        "total": total
    })

def enviar_mail(**kwargs):
    asunto = "Gracias por tu pedido - GestorPedidos"
    mensaje = render_to_string("emails/pedido.html", {
        "pedido": kwargs.get("pedido"),
        "lineas_pedido": kwargs.get("lineas_pedido"),
        "usuario": kwargs.get("usuario"),
        "emailusuario": kwargs.get("email")
    })
    mensaje_texto = strip_tags(mensaje)
    from_email = "xbrand9000@gmail.com"
    to = kwargs.get("email")
    
    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)
