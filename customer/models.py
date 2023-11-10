
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
    has_approved = models.BooleanField(default=False, blank=True, null=True)
    
    class Meta:
        verbose_name = "Vendor" 
         
    def __str__(self):
        return str(self.first_name)
    
STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)

class MultipleAddress(models.Model):
    """Add Multiple Address Model"""
    
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    pincode = models.IntegerField()
    locality = models.CharField(max_length=20)
    address  = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50,choices=STATE_CHOICES)
    landmark  = models.CharField(max_length=30)
    
    # relation
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete= models.CASCADE, null=True, blank=True)
    
    