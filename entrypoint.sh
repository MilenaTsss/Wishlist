#!/bin/sh

echo "Checking for unapplied model changes..."
python manage.py makemigrations --check --dry-run
if [ $? -ne 0 ]; then
  echo "ERROR: There are model changes that are not reflected in migrations!"
  exit 1
fi

echo "No missing migrations found."

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME}'
email = '${DJANGO_SUPERUSER_EMAIL}'
password = '${DJANGO_SUPERUSER_PASSWORD}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
EOF


echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 Wishlist.wsgi:application \
  --access-logfile - \
  --error-logfile - \
  --access-logformat '{"time": "%(t)s", "status": %(s)s, "method": "%(m)s", "url": "%(U)s", "size": %(b)s, "ip": "%(h)s", "user_agent": "%(a)s"}'
