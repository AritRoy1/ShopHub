# import lib
from django.db import models

# import model
from customer.models import Vendor, Customer
# Create your models here.

class CreateDate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    


class Product(CreateDate):
    """Product Model"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    brand = models.CharField(max_length=30, blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
   
    
    ## relation
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
       
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='Product_Images/', max_length=250)    
    
    def __str__(self):  
        return str(self.image)



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    
CHOICES_STATUS = [
    ('Accepted','Accepted'),
    ('Placed','Placed'),
    ('Shipped','Shipped'),
    ('Out for Delevery','Out for Delevery'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ("Pending","Pending")
    
]
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=CHOICES_STATUS, default = "Pending")

    
class Wishlist(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)