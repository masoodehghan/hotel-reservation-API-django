# Generated by Django 4.1 on 2022-08-31 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0008_alter_reservation_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
