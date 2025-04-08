from django.db import models

# Create your models here.

class CategoriaProd(models.Model):
    nombre= models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "CategoriaProd"
        verbose_name_plural = "CategoriasProd"
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    categorias = models.ForeignKey("CategoriaProd", on_delete=models.CASCADE)
    imagen =models.ImageField(upload_to="tienda",null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilidad = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def precio_formateado(self):
        return round(self.precio, 2)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    def __str__(self):
        return f"{self.nombre}" 