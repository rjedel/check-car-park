# Generated by Django 3.1.5 on 2021-01-27 21:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('car_park', '0002_auto_20210120_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opinion',
            name='update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
