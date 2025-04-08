from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from carro.carro import Carro
from pedidos.models import LineaPedido, Pedido
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from carro.carro import Carro

# Create your views here.

@login_required(login_url="/autenticacion/logear")
def procesar_pedido(request):
    pedido = Pedido.objects.create(user=request.user)
    carro = Carro(request)
    lineas_pedido = list()
    for key, value in carro.carro.items():
        lineas_pedido.append(LineaPedido(
            
            producto_id = key,
            cantidad = value["cantidad"],
            user = request.user,
            pedido = pedido
        ))
    LineaPedido.objects.bulk_create(lineas_pedido)
    
    enviar_mail(
        pedido=pedido,
        lineas_pedido = lineas_pedido,
        usuario = request.user.username,
        email = request.user.email
    )
    
    messages.success(request, "El pedido ha sido creado correctamente")
    carro = Carro(request)
    carro.limpiar_carro()
    return redirect("../tienda")
    
def enviar_mail(**kwargs):
    asunto = "Gracias por el pedido, la solicitud del pedido ha sido enviadad"
    mensaje = render_to_string("emails/pedido.html",{
        "pedido" : kwargs.get("pedido"),
        "lineas_pedido" : kwargs.get("lineas_pedido"),
        "usaurio" : kwargs.get("usuario"),
        "emailusuario" : kwargs.get("email")
    }
    )
    mensaje_texto = strip_tags(mensaje)
    from_email = "xbrand9000@gmail.com"
    to = kwargs.get("emailusuario")
    print(to)
    
    send_mail(asunto,mensaje_texto,to,[from_email],html_message=mensaje)