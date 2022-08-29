# Generated by Django 4.1 on 2022-08-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('h', 'Host'), ('g', 'Guest'), ('a', 'Admin')], default='a', max_length=1),
        ),
    ]
