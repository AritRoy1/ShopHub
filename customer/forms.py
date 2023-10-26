from django import forms
from .models import Customer, Vendor, MultipleAddress
from django.db import models
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from django.utils.translation import gettext, gettext_lazy as _

class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.CharField(required=True)
       
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date',
                  'phone_number','address', 'city', 'state', 'zip_code']


class VendorRegistrationForm(UserCreationForm):
    class Meta:
        model = Vendor
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date',
                  'phone_number','address', 'city', 'state', 'zip_code', 'aadhar_number', 'ac_number'
                  , 'gst_invoice']
        
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'phone_number', 'city', 'state', 'address']
        
        widgets = {'address':forms.Textarea(attrs={'cols':34, 'rows':4})}
        
class AddAddressForm(forms.ModelForm):
    class Meta:
        model = MultipleAddress
        fields = ['name', 'phone_number', 'pincode', 'locality', 'address', 'city', 'state', 'landmark']
        widgets = {'address':forms.Textarea(attrs={'cols':34, 'rows':4})}
        
