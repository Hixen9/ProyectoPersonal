from tienda.models import Producto, CategoriaProducto
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

def tienda(request):
    categoria_id = request.GET.get("categoria")
    categorias = CategoriaProducto.objects.all()

    if categoria_id:
        productos_list = Producto.objects.filter(categoria_id=categoria_id)
        categoria_actual = int(categoria_id)
    else:
        productos_list = Producto.objects.all()
        categoria_actual = None

    # PAGINACIÓN: 20 productos por página
    paginator = Paginator(productos_list, 16)  # 20 productos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tienda/tienda.html", {
        "page_obj": page_obj,  # paginador
        "categorias": categorias,
        "categoria_actual": categoria_actual
    })


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = CategoriaProducto.objects.all()  # Si quieres mostrar también el menú de categorías

    return render(request, "tienda/detalle_producto.html", {
        "producto": producto,
        "categorias": categorias,
    })