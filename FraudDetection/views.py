from django.http import HttpResponse
from django.shortcuts import render
import json
from mainImp import fraud_detect
from service.models import customerLoginModel
from service.models import registrationModel
from service.models import garageLoginModel
from service.models import claimQueryModel
from django.core.mail import send_mail

import random

def generate_otp():
    # Generate a 6-digit OTP
    otp = random.randint(100000, 999999)
    return otp

#Claim Processing after sumbmission of query
def processClaim(request):
    if request.method == "POST":
        userEm = request.POST['userEmail']
        sx = request.POST['sex']
        marrytal = request.POST['maritalStatus']
        ag = request.POST['age']
        vehicleP = request.POST['vehiclePrice']
        deduct = request.POST['deductible']
        rating = request.POST['driverRating']
        addressChange = request.POST['addressChangeClaim']
        numberCars = request.POST['numberOfCars']
        garage = request.POST['garageName']

        strML = 'Pending'
        strGarage = 'Pending'



        arrayInput = [sx, marrytal, ag, vehicleP, deduct, rating, addressChange, numberCars]
            
        result = fraud_detect(arrayInput)
        if(result == 0):
            strML = 'Rejected'
        else:
            strML = 'Approved'
            
        en = claimQueryModel(service_username=userEm, service_sex=sx,service_maritalStatus=marrytal,service_age=ag, 
                             service_vehiclePrice=vehicleP
                             , service_deductible=deduct, service_driverRating=rating, 
                             service_addressChangeClaim=addressChange,
                             service_numberOfCars=numberCars, service_Garage_username=garage, service_Garage_Output=strGarage,
                             service_ML_Output=strML,service_final_output=strGarage)
        send_mail(
                    "Car Insurance Query Submitted",
                    "Your Car Insurance Query has been Submitted Successfully. Your Query is in process. Please check the status through login page.",
                    "carinsurancefrauddetection@gmail.com",
                    [userEm],
                    fail_silently=False,
        )
        en.save()
        
    return render(request, "custLogin.html")
#HomePage
def homePage(request):
    return render(request, "index.html")

#Customer Login Page
def customerLogin(request):
    return render(request, "custLogin.html")

#Garage Owner Login Page
def garageLogin(request):
    return render(request, "garageLogin.html")

#Customer Login Form Submission Action
def customerLoginSubmit(request):
    if request.method == "POST":
        user = request.POST['username']
        passw = request.POST['password']
        # en = customerLoginModel(service_username=user, service_password=passw)
        dataArray = registrationModel.objects.all()
        for i in dataArray:
            if i.service_email == user:
                if i.service_password == passw:
                    allQueryData = claimQueryModel.objects.all()
                    restrictedQueryData = []
                    for m in allQueryData:
                        if i.service_email == m.service_username:
                            restrictedQueryData.append(m)
                    
                    usernameRestrictedQueryData = {'restrictedQueryData' : restrictedQueryData, 'userEmail': user} 
                    return render(request, "custPage.html", usernameRestrictedQueryData)
        return HttpResponse("<h1>Invalid Credentials</h1>")
    return render(request, "custLogin.html")

#Customer Options after Login
def custAfterLogin(request):
    return render(request, "custPage.html")


#Customer Claim Request Page
def requestClaim(request):
    if request.method == "POST":
        email = request.POST['object_user_email']
        emailDict = {'userEmail' : email}
        return render(request, "claimQuery.html", emailDict)

#New Customer Registration Page
def customerRegister(request):
    if request.method == "POST":
        name = request.POST['name']
        gender = request.POST['gender']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        # temp = registrationModel(service_name=name, service_gender=gender, service_phone=phone, service_email=email, service_password=password)
        
        otp = generate_otp()
        dataDict = {
            'name':name,
            'gender':gender,
            'phone':phone,
            'email':email,
            'password':password,
            'otp':otp
        }
        strMessage = """Dear """ + name + """,

I hope this email finds you well. Thank you for choosing our Car Insurance System for your insurance needs. To ensure the security of your account and protect your information, we are implementing a two-step verification process.

As part of this process, we have generated a One-Time Password (OTP) for your account. Please use the following OTP to complete the verification:

OTP: """ + str(otp) + """

To complete the verification, follow these steps:

Log in to your Car Insurance System account.
Navigate to the account settings or security section.
Enter the provided OTP when prompted.
Please note that the OTP is valid for a limited time and should be used promptly to avoid any inconvenience.

If you did not initiate this verification or suspect any unauthorized access to your account, please contact our customer support immediately at [Customer Support Email or Phone Number].

We appreciate your cooperation in ensuring the security of your account. Thank you for choosing [Your Company Name] for your car insurance needs.

Best regards,

Car Insurance Fraud Detection Company
"""
        send_mail(
                    "Account Verification - One-Time Password (OTP) for Car Insurance System",
                    strMessage,
                    "carinsurancefrauddetection@gmail.com",
                    [email],
                    fail_silently=False,
        )
        
        return render(request, "otpValidationPage.html", dataDict)
    return render(request, "customerRegister.html")

def afterOPTSubmit(request):
    if request.method == "POST":
        inputOTP = request.POST['otpInput']
        generatedOTP = request.POST['object_otp']

        name = request.POST['object_name']
        gender = request.POST['object_gender']
        phone = request.POST['object_phone']
        email = request.POST['object_email']
        password = request.POST['object_password']

        temp = registrationModel(service_name=name, service_gender=gender, service_phone=phone, service_email=email, service_password=password)
        
        if inputOTP == generatedOTP:
            temp.save()
            return render(request, "custLogin.html")
        else:
            return HttpResponse("Wrong OPT")
    return HttpResponse("TRU/e OPT")

#After login, garage page
def garagePage(request):
    if request.method == "POST":
        user = request.POST['garageEmail']
        passw = request.POST['garagePass']
        # en = customerLoginModel(service_username=user, service_password=passw)
        dataArray = garageLoginModel.objects.all()


        for i in dataArray:
            if i.service_username == user:
                if i.service_password == passw:
                    allQueryData = claimQueryModel.objects.all()
                    restrictedQueryData = []
                    for m in allQueryData:
                        if i.service_username == m.service_Garage_username:
                            if m.service_Garage_Output == 'Pending':
                                restrictedQueryData.append(m)
                    
                    usernameRestrictedQueryData = {'restrictedQueryData' : restrictedQueryData} 
                    

                    return render(request, "garagePage.html", usernameRestrictedQueryData)
        return HttpResponse("<h1>Invalid Credentials</h1>")
    # return render(request, "garagePage.html")

#Garage after taking input of correct or wrong.
def garagePageAfterInput(request):
    if request.method == 'POST':
        form_email = request.POST['object_email']
        form_age = request.POST['object_age']
        form_price = request.POST['object_price']
        form_garage_email = request.POST['object_garage_email']
        form_output = request.POST['object_output']

        allQueryData = claimQueryModel.objects.all()

        for i in allQueryData:
            if i.service_username == form_email and i.service_age == form_age and i.service_vehiclePrice == form_price:
                if form_output == 'Correct':
                    i.service_Garage_Output = 'Approved'
                elif form_output == 'Wrong':   
                    i.service_Garage_Output = 'Rejected'
    
                if i.service_ML_Output == 'Approved' and i.service_Garage_Output == 'Approved':
                    i.service_final_output = 'Approved'
                elif i.service_ML_Output == 'Rejected' and i.service_Garage_Output == 'Approved':
                    i.service_final_output = 'Investigating'
                elif i.service_ML_Output == 'Approved' and i.service_Garage_Output == 'Rejected':
                    i.service_final_output = 'Investigating'
                elif i.service_ML_Output == 'Rejected' and i.service_Garage_Output == 'Rejected':
                    i.service_final_output = 'Rejected'
                send_mail(
                    "Approval Status of Your Car Insurance Claim Query",
                    """Dear """ + i.service_username + """,

We hope this email finds you well. We would like to update you on the status of your recent car insurance claim query with Car Insurance Fraud Detection Company.

After thorough review and evaluation of the provided documentation and information, we are pleased to inform your status. We understand the importance of a swift resolution during such circumstances, and we have processed your claim with the utmost efficiency.
Status of the Claim: """ + i.service_final_output + 
"""
Best regards
""",
                    "carinsurancefrauddetection@gmail.com",
                    [i.service_username],
                    fail_silently=False,
                )
                i.save()
                
        allQueryData1 = claimQueryModel.objects.all()
        restrictedQueryData = []
        for m in allQueryData1:
            if form_garage_email == m.service_Garage_username:
                if m.service_Garage_Output == 'Pending':
                    restrictedQueryData.append(m)
                    
        usernameRestrictedQueryData = {'restrictedQueryData' : restrictedQueryData} 
                    

        return render(request, "garagePage.html", usernameRestrictedQueryData)
        
    return HttpResponse("Not ok 200")
        #help(form_data)
        #print(python_object.service_Garage_Output)