from django.db import models

# Create your models here.
from django.core import validators
from product.models import Product
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

    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )
    status = models.CharField(max_length=30, choices=CHOICES_STATUS, default = "Pending")
    

   

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )