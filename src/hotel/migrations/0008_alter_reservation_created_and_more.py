# Generated by Django 4.1 on 2022-08-31 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_alter_reservation_guest_alter_reservation_room_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
