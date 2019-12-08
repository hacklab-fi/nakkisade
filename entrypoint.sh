#!/bin/bash

django-admin compilemessages
echo "Applying database migrations"
python manage.py migrate --run-syncdb

echo "Creating superuser"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${ADMIN_USER:-admin}', '${ADMIN_EMAIL:-admin@email.invalid}', '${ADMIN_PASSWORD:-password}')" | python manage.py shell

echo "Starting server"
python -u manage.py runserver 0.0.0.0:8000 --noreload

