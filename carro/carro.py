#"""Tareas a realizar del carro
# Manjeo de sesion:
# tiene que ser capaz de manejar la sesion en django
# en este apartado vamos a realizar una clase Carro para poder tener control sobre el carro cuando el usuario inicia sesion
# cuando vamos agregando articulos al carro y por algun motivo salimos de la pagina, el carro debe de conservar los articulos
# antes de salir de la pagina de la tienda
# 
# --->agregar productos
# --->eliminar productos:
# elimina la cantidad del producto del carro   
# --->restar productos:
# quita solo una cantidad del producto seleccionado
# --->vaciar carro:
# elimina  los productos del carro
# """"
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP

class Carro:
    #Manejo de sesion
    # el request es la petición
    # lo que queremos es almacenar la petición actual para utilizarlo mas adelante
    def __init__(self,request):
        #tenemos que igualar la sesion con el carro
        self.request=request
        self.session=request.session
        #adjudicamos "carro" a la sesion para que identifique el str con el carro
        #METODO CONSTRUCTOR
        carro = self.session.get("carro")
        #si la sesion iniciada no tiene carro, creamos un nuevo carro para el usuario
        if not carro:
            carro = self.session["carro"]={}
        #y si el usuario estaba agregando productos se fue y vuelve, SI HAY CARRO entonces... el carro es igual al carro que ya habia
        self.carro = carro
    
    
    def agregar(self,producto):
          # convierto el precio del producto a Decimal con dos decimales
        precio_unitario = Decimal(str(producto.precio)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        if str(producto.id) not in self.carro:
            # Primer agregado: guardo precio y cantidad
            self.carro[str(producto.id)] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                # almaceno el precio formateado como cadena, o bien como Decimal si tu sesión lo soporta
                "precio": str(precio_unitario),
                "cantidad": 1,
                "imagen": producto.imagen.url,
            }
        else:
            # Ya existía: incremento cantidad y sumo precio
            entry = self.carro[str(producto.id)]
            entry["cantidad"] += 1

            # Saco el precio actual, lo sumo y vuelvo a redondear
            acumulado = Decimal(entry["precio"]) + precio_unitario
            acumulado = acumulado.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            entry["precio"] = str(acumulado)

        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
    
    def eliminar(self,producto):
        producto.id = str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()
            
    def restar_producto(self,producto):
        for key, entry in self.carro.items():
            if key == str(producto.id):
                # Reducimos la cantidad
                entry["cantidad"] -= 1

                # Precio unitario formateado a 2 decimales
                precio_unitario = Decimal(str(producto.precio)).quantize(
                    Decimal("0.00"), rounding=ROUND_HALF_UP
                )

                # Calculamos el nuevo precio acumulado
                acumulado = Decimal(entry["precio"]) - precio_unitario

                # Redondeamos de nuevo a 2 decimales
                acumulado = acumulado.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

                # Guardamos como cadena para evitar problemas de serialización
                entry["precio"] = str(acumulado)

                # Si ya no queda ninguno, lo eliminamos
                if entry["cantidad"] < 1:
                    self.eliminar(producto)
                break

        self.guardar_carro()
    
    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified = True
                   
        