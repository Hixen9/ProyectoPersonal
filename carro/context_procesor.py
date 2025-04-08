# estamos creando una variable global
from decimal import Decimal
def importe_total_carro(request):
    total=0
    if request.user.is_authenticated:
        for key,value in request.session["carro"].items():
            total += float(value["precio"])
    else:
        total="Debes de hacer Login"
    return {"importe_total_carro":total}