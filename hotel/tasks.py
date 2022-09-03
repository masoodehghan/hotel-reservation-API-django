from hotel_reservation.celery import app
from .api.v1.models import Reservation
from django.utils import timezone
from celery.utils.log import logger


@app.task(name='reservation_deletion')
def remove_old_reservations():
    Reservation.objects.filter(end_date__lt=timezone.now().date()).delete()
    logger.info('deleted reservations successfully.')
