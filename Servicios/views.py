from django.shortcuts import render

def servicios(request):
    return render(request,"Servicios/servicios.html",{"Servicios":servicios})
