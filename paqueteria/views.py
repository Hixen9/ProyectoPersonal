
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from pedidos.models import EstadoPedido, Pedido, Paqueteria
from tienda.models import Producto
from carro.models import LineaPedido
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def paqueteria_dashboard(request):
    pedidos = EstadoPedido.objects.all()

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        recoleccion = request.POST.get("recoleccion") == "on"
        envio = request.POST.get("envio") == "on"
        entregado = request.POST.get("entregado") == "on"

        try:
            estado = EstadoPedido.objects.get(pedido_id=pedido_id)
        except EstadoPedido.DoesNotExist:
            messages.error(request, "No se encontró un EstadoPedido para el pedido seleccionado.")
            return redirect("paqueteria_dashboard")

        pedido_obj = get_object_or_404(Pedido, id=pedido_id)
        usuario = pedido_obj.user
        lineas = LineaPedido.objects.filter(pedido=pedido_obj)

        productos = []
        for linea in lineas:
            try:
                producto_obj = Producto.objects.get(nombre__iexact=linea.producto.strip())
                productos.append({
                    "producto": producto_obj,
                    "cantidad": linea.cantidad
                })
            except Producto.DoesNotExist:
                # Usar fallback para productos no encontrados
                productos.append({
                    "producto": type("ProductoMock", (), {
                        "nombre": linea.producto,
                        "imagen": None,
                        "precio": 0
                    })(),
                    "cantidad": linea.cantidad
                })

        prev_recoleccion = estado.proceso_recoleccion
        prev_envio = estado.proceso_envio
        prev_entregado = estado.entregado

        # Validaciones de secuencia
        if envio and not (recoleccion or prev_recoleccion):
            messages.error(request, "Para marcar 'En ruta', primero debe estar en recolección.")
            return redirect("paqueteria_dashboard")

        if entregado and not ((recoleccion or prev_recoleccion) and (envio or prev_envio)):
            messages.error(request, "Para marcar 'Entregado', primero debe estar en recolección y en ruta.")
            return redirect("paqueteria_dashboard")

        estado.proceso_recoleccion = recoleccion
        estado.proceso_envio = envio
        estado.entregado = entregado
        estado.save()

        domain = "http://127.0.0.1:8000"

        if recoleccion and not prev_recoleccion:
            enviar_estado_mail(pedido=pedido_obj, productos=productos, usuario=usuario, email=usuario.email, estado_actual="en proceso de recolección", domain=domain)

        if envio and not prev_envio:
            enviar_estado_mail(pedido=pedido_obj, productos=productos, usuario=usuario, email=usuario.email, estado_actual="en ruta", domain=domain)

        if entregado and not prev_entregado:
            enviar_estado_mail(pedido=pedido_obj, productos=productos, usuario=usuario, email=usuario.email, estado_actual="entregado", domain=domain)

        messages.success(request, "Estado del pedido actualizado correctamente.")
        return redirect("paqueteria_dashboard")

    return render(request, "paqueteria/dashboard.html", {"pedidos": pedidos})


def enviar_estado_mail(**kwargs):
    pedido = kwargs.get("pedido")
    productos = kwargs.get("productos")
    usuario = kwargs.get("usuario")
    email = kwargs.get("email")
    estado_actual = kwargs.get("estado_actual")
    domain = settings.SITE_URL

    if not pedido or not email or not productos:
        print("Faltan datos para enviar correo")
        return

    asunto = f"Estado actualizado para tu pedido #{pedido.id} - GestorPedidos"

    mensaje = render_to_string("emails/estado_pedido.html", {
        "pedido": pedido,
        "productos": productos,
        "usuario": usuario,
        "estado_actual": estado_actual,
        "year": datetime.now().year,
        "domain": domain
    })

    mensaje_texto = strip_tags(mensaje)

    send_mail(
        subject=asunto,
        message=mensaje_texto,
        from_email="xbrand9000@gmail.com",
        recipient_list=[email],
        html_message=mensaje,
        fail_silently=False
    )

def paqueteria_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            paquetero = Paqueteria.objects.get(username_paqueteria=username, contraseña_paqueteria=password)
            request.session['paqueteria_id'] = paquetero.id
            request.session['paqueteria_username'] = paquetero.username_paqueteria
            return redirect('paqueteria_dashboard')

        except Paqueteria.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "paqueteria/paqueteria.html")


def paqueteria_logout(request):
    request.session.pop('paqueteria_id', None)
    request.session.pop('paqueteria_username', None)
    return redirect('paqueteria_login')