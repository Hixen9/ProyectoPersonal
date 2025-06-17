#!/usr/bin/env python
import os
import sys
import django
from django.core.management import call_command

# 1) Añade el directorio raíz al path
sys.path.append(os.getcwd())

# 2) Señala tu settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProyectoWeb.settings")

# 3) Inicializa Django
django.setup()

# 4) Volcado en UTF-8 de tus apps + usuarios y permisos
with open("datos.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        # primero los modelos de auth:
        "auth.user",
        "auth.group",
        "auth.permission",
        "contenttypes",        # necesario para las claves foráneas de auth
        # luego tus apps
        "tienda",
        "Servicios",
        "pedidos",
        "carro",
        "blog",
        "autenticacion",
        natural_primary=True,
        natural_foreign=True,
        indent=2,
        stdout=f,
    )

print("✔️ datos.json generado con usuarios y tus apps clave.")
