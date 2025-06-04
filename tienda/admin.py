from django.contrib import admin
from .models import CategoriaProducto,Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'cantidad', 'fecha_creacion', 'fecha_updated')
    readonly_fields = ('fecha_creacion', 'fecha_updated')  # hace que los campos sean visibles pero no editables

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'fecha_updated')
    readonly_fields = ('fecha_creacion', 'fecha_updated')