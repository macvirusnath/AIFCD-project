from django.db import models

class customerLoginModel(models.Model):
    service_username = models.CharField(max_length = 50)
    service_password = models.CharField(max_length = 50)

class registrationModel(models.Model):
    service_name = models.CharField(max_length = 100)
    service_gender = models.CharField(max_length = 50)
    service_phone = models.CharField(max_length = 50)
    service_email = models.CharField(max_length = 50)
    service_password = models.CharField(max_length = 50)

class garageLoginModel(models.Model):
    service_username = models.CharField(max_length = 50)
    service_password = models.CharField(max_length = 50)

class claimQueryModel(models.Model):
    service_username = models.CharField(max_length = 50)
    service_sex = models.CharField(max_length = 50)
    service_maritalStatus = models.CharField(max_length = 50)
    service_age = models.CharField(max_length = 50)
    service_vehiclePrice = models.CharField(max_length = 50)
    service_deductible = models.CharField(max_length = 50)
    service_driverRating = models.CharField(max_length = 50)
    service_addressChangeClaim = models.CharField(max_length = 50)
    service_numberOfCars = models.CharField(max_length = 50)
    service_ML_Output = models.CharField(max_length = 50)
    service_Garage_Output = models.CharField(max_length = 50)
    service_Garage_username = models.CharField(max_length = 50)
    service_final_output = models.CharField(max_length = 50)

# Create your models here.
