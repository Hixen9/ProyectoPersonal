from django.urls import path
from ProyectoWebApp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="Home"),
]

#Agregamos a la lista urlpatterns la funcion static para mostrar los archivos media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)