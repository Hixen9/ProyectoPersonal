from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Puedes luego cambiar a ForeignKey
    fecha = models.DateTimeField(auto_now_add=True)

class Recibo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    precio_total = models.FloatField()

class Paqueteria(models.Model):
    username_paqueteria = models.CharField(max_length=255, unique=True)
    contraseña_paqueteria = models.CharField(max_length=20)

class EstadoPedido(models.Model):
    username_paqueteria = models.CharField(max_length=255)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)  # ✅ RELACIÓN REAL
    pedido_confirmado = models.BooleanField(default=False)
    proceso_recoleccion = models.BooleanField(default=False)
    proceso_envio = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)