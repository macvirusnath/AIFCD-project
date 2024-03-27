from django.contrib import admin

# Register your models here.
from service.models import customerLoginModel
from service.models import registrationModel
from service.models import garageLoginModel
from service.models import claimQueryModel

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('service_username','service_password')



class RegisterationAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_gender', 'service_phone', 'service_email', 'service_password')

class GarageLoginAdmin(admin.ModelAdmin):
    list_display = ('service_username','service_password')


class ClaimQueryAdmin(admin.ModelAdmin):
    list_display = ('service_username', 'service_sex','service_maritalStatus', 'service_age', 'service_vehiclePrice', 'service_deductible',
                    'service_driverRating', 'service_addressChangeClaim', 'service_numberOfCars','service_ML_Output',
                    'service_Garage_Output', 'service_Garage_username', 'service_final_output',)


admin.site.register(customerLoginModel, CustomerAdmin)
admin.site.register(registrationModel, RegisterationAdmin)
admin.site.register(garageLoginModel, GarageLoginAdmin)
admin.site.register(claimQueryModel, ClaimQueryAdmin)

