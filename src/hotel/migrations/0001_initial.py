# Generated by Django 4.1 on 2022-08-29 20:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hotel.api.v1.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(default='')),
                ('host', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('country', models.CharField(max_length=40)),
                ('city', models.CharField(max_length=40)),
                ('district', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(default='', max_length=20)),
                ('number_of_rooms', models.PositiveSmallIntegerField()),
                ('number_of_adult_beds', models.PositiveSmallIntegerField()),
                ('number_of_child_beds', models.PositiveSmallIntegerField()),
                ('floor', models.PositiveSmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MaxValueValidator(100.0)])),
                ('description', models.TextField(default='')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotel.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='hotel.location'),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=hotel.api.v1.models.photo_path)),
                ('object_id', models.PositiveBigIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddIndex(
            model_name='gallery',
            index=models.Index(fields=['object_id', 'content_type'], name='hotel_galle_object__fb6fca_idx'),
        ),
    ]