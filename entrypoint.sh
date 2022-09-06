python manage.py runserver 0.0.0.0:8000 &
celery -A hotel_reservation worker -l INFO &
celery -A hotel_reservation beat -l INFO -s /tmp/celerybeat-schedule