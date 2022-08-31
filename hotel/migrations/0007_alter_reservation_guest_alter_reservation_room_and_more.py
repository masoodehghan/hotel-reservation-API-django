# Generated by Django 4.1 on 2022-08-31 11:05

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0006_reservation_is_canceled_reservation_is_refund_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='guest',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hotel.room'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 8, 31, 11, 5, 29, 340213, tzinfo=datetime.timezone.utc))]),
        ),
    ]
