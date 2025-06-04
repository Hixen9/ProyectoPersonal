from django.db import models

# Create your models here.
class LineaPedido(models.Model):
    username = models.CharField(max_length=255)
    producto = models.CharField(max_length=255)
    pedido = models.CharField(max_length=255)
    cantidad = models.IntegerField()