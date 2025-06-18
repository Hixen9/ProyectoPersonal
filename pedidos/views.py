from datetime import datetime
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
from pedidos.models import EstadoPedido,Paqueteria,Recibo
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url="/autenticacion/logear")
def procesar_pedido(request):
    carro = Carro(request)
    usuario = request.user

    # Crear el pedido
    pedido = Pedido.objects.create(user=usuario)

    lineas_pedido = []

    for key, value in carro.carro.items():
        try:
            producto_obj = Producto.objects.get(id=key)
        except Producto.DoesNotExist:
            continue

        # Guardamos solo el nombre del producto como texto
        linea = LineaPedido(
            username=usuario.username,
            producto=producto_obj.nombre,  # ← TEXT
            pedido=pedido,
            cantidad=value["cantidad"]
        )
        lineas_pedido.append(linea)

        # Actualizar stock
        producto_obj.cantidad -= value["cantidad"]
        if producto_obj.cantidad <= 0:
            producto_obj.disponibilidad = False
        producto_obj.save()

    LineaPedido.objects.bulk_create(lineas_pedido)

    # Obtener paquetería por defecto
    try:
        paqueteria = Paqueteria.objects.get(username_paqueteria="Estafeta")
        username_paqueteria = paqueteria.username_paqueteria
    except Paqueteria.DoesNotExist:
        username_paqueteria = ''

    EstadoPedido.objects.create(
        username=usuario,
        pedido=pedido,
        username_paqueteria=username_paqueteria,
        pedido_confirmado=True,
        proceso_recoleccion=False,
        proceso_envio=False,
        entregado=False
    )

    # Crear recibos
    recibos = []
    total = 0
    for linea in lineas_pedido:
        try:
            producto_obj = Producto.objects.get(nombre__iexact=linea.producto.strip())
            subtotal = producto_obj.precio * linea.cantidad
            total += subtotal
            recibos.append(Recibo(
                usuario=usuario,
                producto=producto_obj.nombre,
                cantidad=linea.cantidad,
                precio_total=subtotal
            ))
        except Producto.DoesNotExist:
            continue

    Recibo.objects.bulk_create(recibos)

    # Preparar datos del correo
    lineas_correo = []
    for linea in lineas_pedido:
        try:
            producto_obj = Producto.objects.get(nombre__iexact=linea.producto.strip())
            lineas_correo.append({
                "producto": producto_obj,
                "cantidad": linea.cantidad,
                "subtotal": producto_obj.precio * linea.cantidad
            })
        except Producto.DoesNotExist:
            continue

    enviar_mail(
        pedido=pedido,
        lineas_pedido=lineas_correo,
        usuario=usuario.username,
        email=usuario.email,
        total=total,
    )

    messages.success(request, "El pedido ha sido creado correctamente")
    carro.limpiar_carro()

    return render(request, "resumen_pedido.html", {
        "pedido": pedido,
        "lineas": lineas_pedido,
        "total": total
    })

    
def enviar_mail(**kwargs):
    pedido = kwargs.get("pedido")
    lineas_pedido = kwargs.get("lineas_pedido")
    usuario = kwargs.get("usuario")
    email = kwargs.get("email")
    total = kwargs.get("total")
    domain = settings.SITE_URL  # por defecto para desarrollo

    asunto = f"Gracias por tu pedido #{pedido.id} - GestorPedidos"

    mensaje = render_to_string("emails/pedido.html", {
        "pedido": pedido,
        "lineas_pedido": lineas_pedido,
        "usuario": usuario,
        "emailusuario": email,
        "total": total,
        "year": datetime.now().year,
        "domain": domain
    })

    mensaje_texto = strip_tags(mensaje)
    from_email = "xbrand9000@gmail.com"
    to = kwargs.get("email")

    send_mail(asunto, mensaje_texto, from_email, [to], html_message=mensaje)
