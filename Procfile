release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn graduateWork.wsgi --log-file -