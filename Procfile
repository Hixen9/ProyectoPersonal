# Procfile

# Esta sección se ejecuta justo después del build, antes de arrancar tu app
release: python manage.py migrate && python manage.py loaddata datos.json --no-input && python manage.py collectstatic --noinput

# Esto arranca tu servidor
web: gunicorn ProyectoWeb.wsgi:application --bind 0.0.0.0:$PORT
