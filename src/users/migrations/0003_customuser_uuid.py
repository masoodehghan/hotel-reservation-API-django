# Generated by Django 4.1 on 2022-08-30 07:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
