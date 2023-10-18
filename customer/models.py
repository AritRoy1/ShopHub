
# import lib
from django.contrib.auth.models import AbstractUser

#import models
from django.db import models

# Create your models here.

class User(AbstractUser):
    """AbstractUser Model"""
    
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    zip_code = models.IntegerField(null=True)
    
    
class Customer(User):
    """Customer Model"""
    
    class Meta:
        verbose_name = "Customer"
   
    
class Vendor(User):
    """Vendor Model"""
    aadhar_number = models.CharField(max_length=12)
    ac_number = models.CharField(max_length=20)
    gst_invoice = models.FileField(upload_to='Vendor_Gst_Images/', max_length=250)
    
    class Meta:
        verbose_name = "Vendor" 
         
    def __str__(self):
        return str(self.first_name)
    


