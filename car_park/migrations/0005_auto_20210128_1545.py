# Generated by Django 3.1.5 on 2021-01-28 14:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_park', '0004_savedusercarpark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedusercarpark',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notatki'),
        ),
        migrations.AlterUniqueTogether(
            name='savedusercarpark',
            unique_together={('user_id', 'car_park_id')},
        ),
    ]
