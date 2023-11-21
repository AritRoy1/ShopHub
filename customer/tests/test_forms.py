from django.test import SimpleTestCase, TestCase

from customer.forms import CustomerProfileForm, CustomerRegistrationForm, LoginForm , AddAddressForm
from customer.models import Customer, Vendor

class TestForms(TestCase):  
    def setUp(self):
        self.customer=Customer.objects.create(
            username= "aaju1",
            first_name ="ajad",
            last_name= 'sarkar',
            email ="jhgfds@gmail.com",
            birth_date= "2001-9-5",
            phone_number= "7617354120",
            address ="bhopal",
            city ='Indore',
            state ="M.P",
            zip_code= 460440 
        )
        self.vendor=Vendor.objects.create(
            username= "aaju2",
            first_name ="ajad",
            last_name= 'sarkar',
            email ="jhgfds@gmail.com",
            birth_date= "2001-9-5",
            phone_number= "7617354120",
            address ="bhopal",
            city ='Indore',
            state ="M.P",
            zip_code= 460440 ,
            aadhar_number=87654,
            ac_number=987654,
            gst_invoice = 'path/to/your/gst_invoice.jpg',
            has_approved = True
        )
        
        
         
    
    def test_customer_profile_form_valid_data(self):
        form_data = {
            'username': 'user12',
            'first_name': 'Arit',
            'last_name': 'Roy',
            'email': 'arit@gmail.com',
            'birth_date': '2000-01-01',
            'phone_number': '1234567890',
            'address': 'Badalpur',
            'city': 'City',
            'state': 'State',
            'zip_code': '12345',
            "password1":"pass12345",
            "password2":"pass12345",    
        }

        form = CustomerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_customer_profile_form_invalid_data(self):
        form = CustomerRegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),12)
        
            
    def test_login_form_valid_data(self):
        form_data = {
            'username': 'user',
            'password': 'password123',
        }

        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid())
        
    def test_login_form_invalid_data(self):
        form_data = {
            'username': 'testuser',
           
        }

        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        
    def test_customer_profile_form_valid_data(self):
        form_data = {
            'first_name': 'Arit',
            'last_name': 'Roy',
            'email': 'jjgahsh@gmail.com',
            'birth_date': '2000-01-01',
            'phone_number': '128765587',
            'city': 'City',
            'state': 'State',
            'address': 'Fulberiya',
        }

        form = CustomerProfileForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_customer_profile_form_invalid(self):

        form = CustomerProfileForm(data={})

        self.assertFalse(form.is_valid())

    # #error
    
    def test_add_address_form_valid_data(self):    
        form_data = {
            'name': 'Pankaj udas',
            'phone_number': '1234567890',
            'pincode': 460440,
            'locality': 'Indian',
            'address': 'Chopna oh nghjg hgj',
            'city': 'Betul',
            'state': 'AS',
            'landmark': 'lkjhg',        
        }

        form = AddAddressForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_add_address_form_invalid_data(self):
        form = AddAddressForm(data={})
        self.assertFalse(form.is_valid())
    