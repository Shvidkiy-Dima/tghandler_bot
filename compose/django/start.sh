#!/bin/bash


python /app/check_conn.py --service-name db --port 5432  --ip db

python /app/manage.py makemigrations
python /app/manage.py migrate --fake-initial
cd /app

python manage.py runserver 0.0.0.0:8000



