from django import forms
from .models import Product
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from customer.models import Vendor

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"



class VendorRegistrationForm(UserCreationForm):
    class Meta:
        model = Vendor
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date',
                  'phone_number','address', 'city', 'state', 'zip_code', 'aadhar_number', 'ac_number'
                  , 'gst_invoice']
        widgets = {'address':forms.Textarea(attrs={'cols':34, 'rows':4})}
        