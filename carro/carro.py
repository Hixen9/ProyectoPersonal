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
        #realizamos una comprobacion para saber si el producto existe todavia
        if(str(producto.id) not in self.carro.keys()):
            #La entrada tiene como clave el id del producto y como valor un diccionario
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio":str(producto.precio),
                "cantidad":1,
                "imagen":producto.imagen.url
            }
        else:
            for key,value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"] = value["cantidad"] + 1
                    value["precio"] = Decimal(value["precio"]) + producto.precio
                    value["precio"] = float(value["precio"])
                    break
                    
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
        for key,value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"] = value["cantidad"] - 1
                    value["precio"] = Decimal(value["precio"]) - producto.precio
                    value["precio"] = float(value["precio"])
                    if value["cantidad"] < 1:
                        self.eliminar(producto)
                    break
        self.guardar_carro()
    
    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified = True
                   
        