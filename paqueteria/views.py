from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from pedidos.models import EstadoPedido
from pedidos.models import Paqueteria  # O la app donde tengas el modelo Paqueteria

def paqueteria_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            paquetero = Paqueteria.objects.get(username_paqueteria=username, contraseña_paqueteria=password)
            # Guardamos sesión manual
            request.session['paqueteria_id'] = paquetero.id
            request.session['paqueteria_username'] = paquetero.username_paqueteria
            return redirect('paqueteria_dashboard')

        except Paqueteria.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "paqueteria/paqueteria.html")


def paqueteria_dashboard(request):
    # Validamos que la sesión de Paquetería esté activa
    if 'paqueteria_id' not in request.session:
        return redirect('paqueteria_login')

    # Obtener pedidos (puedes personalizar para que solo vea los suyos si manejas paquetería por UsernamePaqueteria)
    pedidos = EstadoPedido.objects.all()

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        en_transito = 'en_transito' in request.POST
        entregado = 'entregado' in request.POST

        estado = EstadoPedido.objects.get(id=pedido_id)
        estado.ProcesoEnvio = en_transito
        estado.Entregado = entregado
        estado.save()

        messages.success(request, "Estado del pedido actualizado correctamente.")

    return render(request, "paqueteria/dashboard.html", {"pedidos": pedidos})


def paqueteria_logout(request):
    # Limpiamos la sesión de paquetería
    request.session.pop('paqueteria_id', None)
    request.session.pop('paqueteria_username', None)
    return redirect('paqueteria_login')
