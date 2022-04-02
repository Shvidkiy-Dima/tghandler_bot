#!/bin/bash


sleep 2

python /app/check_conn.py --service-name db --port 5432  --ip db
python /app/check_conn.py --service-name django --port 8000  --ip django

python /app/bot/run_polling.py