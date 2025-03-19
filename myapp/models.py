from django.db import models

# Create your models here.
# class BiometricField(models.Model):
#     def init(self, *args, **kwargs):
#         kwargs['max_length'] = 1000
#         super().init(*args, **kwargs)
#     def db_type(self, connection):
#         return 'binary'
class Dummy(models.Model):
    username=models.CharField(max_length=10)
    fp=models.CharField(max_length=1000)
class Patient(models.Model):
    adhno=models.CharField(max_length=12)
    pswd=models.CharField(max_length=500,default="!@#$")
    otp=models.CharField(max_length=6,default="******")
    pname=models.CharField(max_length=500)
    pincode=models.CharField(max_length=6)
    state=models.CharField(max_length=50)
    dist=models.CharField(max_length=60)
    Address=models.CharField(max_length=100)
    gender=models.CharField(max_length=20)
    dob=models.CharField(max_length=15)
    diab=models.CharField(max_length=10)
    bp=models.CharField(max_length=10)
    weight=models.CharField(max_length=10)
    height=models.CharField(max_length=10)
    phno=models.CharField(max_length=20)
    emial=models.CharField(max_length=100)
class Hospital(models.Model):
    hid=models.CharField(max_length=50)
    hnumber=models.CharField(max_length=20,default="-")
    otp=models.CharField(max_length=6,default="******")
    pswd=models.CharField(max_length=500,default="!@#$")
    hmail=models.CharField(max_length=500,default="hospital@gmail.com")
    hname=models.CharField(max_length=500)
    pincode=models.CharField(max_length=6)
    state=models.CharField(max_length=50)
    dist=models.CharField(max_length=60)
    Address=models.CharField(max_length=100)
    speciality=models.CharField(max_length=100)
class DiagCenter(models.Model):
    dcid=models.CharField(max_length=50)
    dnumber=models.CharField(max_length=15,default="0000000000")
    pswd=models.CharField(max_length=500,default="!@#$")
    otp=models.CharField(max_length=6,default="******")
    dmail = models.CharField(max_length = 200, default="hospital@gmail.com")
    dcname=models.CharField(max_length=500)
    pincode=models.CharField(max_length=6)
    state=models.CharField(max_length=50)
    dist=models.CharField(max_length=60)
    Address=models.CharField(max_length=100)
class PatientDetails(models.Model):
    date=models.CharField(max_length=50)
    disease=models.CharField(max_length=400)
    diagnosis=models.CharField(max_length=500)
    #prescription=models.CharField(max_length=1000)
    remarks=models.CharField(max_length=500)
    adhno=models.CharField(max_length=12)
    hid=models.CharField(max_length=50)
    hname=models.CharField(max_length=50)
    dname=models.CharField(max_length=100,default="******")

class pdfs(models.Model):
    date=models.CharField(max_length=50)
    hid=models.CharField(max_length=50)
    mid=models.CharField(max_length=50,default="0")
    hname=models.CharField(max_length=50)
    pdf=models.FileField(upload_to='pdfs/', blank=True)
    pdfname=models.CharField(max_length=50,default="-")
    adhno=models.CharField(max_length=12)
class Pres(models.Model):
    date=models.CharField(max_length=50)
    hid=models.CharField(max_length=50)
    mid=models.CharField(max_length=50,default="0")
    hname=models.CharField(max_length=50)
    medicine=models.CharField(max_length=500, blank=True)
    time=models.CharField(max_length=50)
    lunch=models.CharField(max_length=50,default="Anytime") 
    adhno=models.CharField(max_length=12)
class image(models.Model):
    date=models.CharField(max_length=50)
    hid=models.CharField(max_length=50)
    hname=models.CharField(max_length=50)
    img=models.ImageField(upload_to='images/',blank=True) 
    adhno=models.CharField(max_length=12)
class ppdfs(models.Model):
    adhno=models.CharField(max_length=50)
    pdf=models.FileField(upload_to='pdfs/', blank=True)
    pdfname=models.CharField(max_length=50)
