from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(OrderDetail)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product','has_paid', 'status', 'updated_on']
    