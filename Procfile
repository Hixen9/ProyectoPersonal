# Procfile

# 1) RELEASE: se ejecuta sólo una vez al desplegar (antes de arrancar web)
release: python manage.py migrate && \
         python manage.py loaddata datos.json && \
         python manage.py collectstatic --noinput

# 2) WEB: arranca tu aplicación Django en producción
web: gunicorn ProyectoWeb.wsgi:application --bind 0.0.0.0:$PORT
