
# Create your views here.
# views.py
from django.shortcuts import redirect, render
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from pedidos.views import procesar_pedido
from carro.carro import Carro
from django.contrib import messages
from tienda.models import Producto
from django.utils import timezone


@login_required(login_url="/autenticacion/logear")
def checkout(request):
    carro = Carro(request)

    if not carro.carro:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("tienda")

    # Verificar si hay algún producto sin stock
    for item in carro.carro.values():
        try:
            producto = Producto.objects.get(id=item["producto_id"])
        except Producto.DoesNotExist:
            messages.error(request, f"El producto con ID {item['producto_id']} ya no existe.")
            return redirect("Tienda")

        if producto.cantidad < item["cantidad"]:
            messages.error(request, f"El producto '{producto.nombre}' no tiene suficiente stock.")
            return redirect("Tienda")

    # Si todo está bien, proceder con el total y formulario de PayPal
    total = sum(float(item["precio"]) for item in carro.carro.values())
    total = f"{total:.2f}"

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": f"Pedido de {request.user.username}",
        "invoice": f"{request.user.id}-{timezone.now().timestamp()}",
        "currency_code": "MXN",
        "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
        "return_url": request.build_absolute_uri(reverse("pago_exitoso")),
        "cancel_return": request.build_absolute_uri(reverse("pago_cancelado")),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, "checkout.html", {
        "total": total,
        "form": form,
    })

def pago_exitoso(request):
    # Llamamos directamente a la función completa que ya tienes
    return procesar_pedido(request)

def pago_cancelado(request):
    return render(request, "pago_cancelado.html")
