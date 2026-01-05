release: python manage.py collectstatic --noinput
web: gunicorn myproject.wsgi --bind 0.0.0.0:$PORT