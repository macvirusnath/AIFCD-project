# Generated by Django 5.0 on 2023-12-30 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_garageloginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='claimQueryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_sex', models.CharField(max_length=50)),
                ('service_maritalStatus', models.CharField(max_length=50)),
                ('service_age', models.CharField(max_length=50)),
                ('service_vehiclePrice', models.CharField(max_length=50)),
                ('service_deductible', models.CharField(max_length=50)),
                ('service_driverRating', models.CharField(max_length=50)),
                ('service_addressChangeClaim', models.CharField(max_length=50)),
                ('service_numberOfCars', models.CharField(max_length=50)),
            ],
        ),
    ]