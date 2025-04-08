from django.contrib import admin
from Servicios.models import Servicio

#Registro de modelos

#En esta clase ServicioAdmin creamos una variable readonly_fields "solo lectura"
#para los atributos de la BD de created y updated ya que son automaticos de tipo date

class ServicioAdmin(admin.ModelAdmin):
    readonly_fields =("created","updated")

#ademas con esta linea de codigo metemos desde models.py la clase Servicio y
#desde admin.py metemos la clase ServicioAdmin que se creo

admin.site.register(Servicio,ServicioAdmin)
