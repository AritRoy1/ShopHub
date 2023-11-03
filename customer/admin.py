from django.contrib import admin
from .models import User, Customer, Vendor, MultipleAddress

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'password', 'address']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'password',]
    
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'has_approved','password']

@admin.register(MultipleAddress)
class MultipleAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','phone_number', 'pincode', 'locality', 'address', 'city', 'state', 'customer','vendor']
    
   