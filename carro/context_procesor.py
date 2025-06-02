

# estamos creando una variable global
def importe_total_carro(request):
    total = 0.0
    if request.user.is_authenticated:
        for key, value in request.session["carro"].items():
            total += float(value["precio"])
        # formateo a cadena con 2 decimales
        total_str = f"{total:.2f}"
    else:
        total_str = "Debes hacer Login"

    return {"importe_total_carro": total_str}