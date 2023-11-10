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
    name = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
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
    image = models.ImageField(upload_to='Product_Images/', max_length=250)    
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    
    def __str__(self):  
        return str(self.image)


class Cart(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    
    # relation 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    
class Wishlist(models.Model):
    
    # relation
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

