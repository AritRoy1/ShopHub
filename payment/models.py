from django.db import models

# Create your models here.
from django.core import validators
from product.models import Product
from customer.models import Customer
# Create your models here.

    
CHOICES_STATUS = [
    ('Accepted','Accepted'),
    ('Placed','Placed'),
    ('Shipped','Shipped'),
    ('Out for Delevery','Out for Delevery'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ("Pending","Pending")    
]

class OrderDetail(models.Model):

    # You can change as a Foreign Key to the user model
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )
    status = models.CharField(max_length=30, choices=CHOICES_STATUS, default = "Placed")
    
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )
    session_id = models.CharField(max_length=100, null=True, blank=True)

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )
    
    
REASION_FOR_CANCEL=[
    ("EXD","Expected delivery date has changed and the product is arriving at a later date."),
    ('PRA.',"Product is not required anymore."),
    ('change my mind', 'Change My Mind'),
    ('BR', 'Bad review from friends/relatives after ordering the product.')
    
    
]

class CancelOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reasion = models.CharField(max_length=100, choices=REASION_FOR_CANCEL)