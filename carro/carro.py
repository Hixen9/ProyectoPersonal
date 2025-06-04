from decimal import Decimal, ROUND_HALF_UP

class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        # Si no hay carro en la sesión, se inicializa
        self.carro = self.session.get("carro", {})
        if "carro" not in self.session:
            self.session["carro"] = self.carro

    def agregar(self, producto):
        precio_unitario = Decimal(str(producto.precio)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        producto_id = str(producto.id)

        if producto_id not in self.carro:
            # Nuevo producto agregado
            self.carro[producto_id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": str(precio_unitario),
                "cantidad": 1,
                "imagen": producto.imagen.url,
            }
        else:
            # Producto ya en el carro: aumentar cantidad y precio total
            entry = self.carro[producto_id]
            entry["cantidad"] += 1
            acumulado = Decimal(entry["precio"]) + precio_unitario
            entry["precio"] = str(acumulado.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))

        self.guardar_carro()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()

    def restar_producto(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            entry = self.carro[producto_id]
            entry["cantidad"] -= 1

            precio_unitario = Decimal(str(producto.precio)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            acumulado = Decimal(entry["precio"]) - precio_unitario
            entry["precio"] = str(acumulado.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))

            if entry["cantidad"] < 1:
                self.eliminar(producto)
            else:
                self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

                   
        