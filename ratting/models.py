from django.db import models
from customer.models import Customer
from product.models import Product

# Create your models here.

class Ratting(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    ratting = models.IntegerField(default=0)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    