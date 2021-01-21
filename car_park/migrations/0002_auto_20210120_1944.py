# Generated by Django 3.1.5 on 2021-01-20 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_park', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tariffs_name', models.CharField(blank=True, max_length=100)),
                ('first_hour_fee', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('maximum_additional_fee', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('additional_fee_description', models.TextField(blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='carpark',
            name='price_list',
        ),
        migrations.DeleteModel(
            name='PriceList',
        ),
        migrations.AddField(
            model_name='carpark',
            name='tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='car_park.tariff'),
        ),
    ]