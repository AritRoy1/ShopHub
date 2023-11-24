from django.test import TestCase, Client
from unittest.mock import ANY, patch
from unittest import mock
from django.urls import reverse
from customer.models import *
from customer.forms import *
from product.models import *
from ratting.models import *
from .models import OrderDetail
from datetime import datetime
from django.http import HttpResponse


class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username = "user", password="password")
        self.customer = Customer.objects.create(
            username= "aaju10",
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
        self.vendor = Vendor.objects.create(
                username= "aaju5",
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
        
        self.category = Category.objects.create(
                name  = "Electronics",
                vendor = self.vendor
            )
    
        self.subcategory = SubCategory.objects.create(
            name = "laptop",
            category = self.category
            ) 
        
        self.product = Product.objects.create(
            name = "Buds",
            description = "kjhgfddfgh",
            price = 1000.00,
            brand = 'Oneplus',
            color = "black",
            vendor = self.vendor,
            category = self.category,
            sub = self.subcategory
        )
        self.order = OrderDetail.objects.create(
            customer = self.customer,
            product = self.product,
            amount = 12,
            status= "Placed",
            has_paid =True,
            session_id= "123456789",
            order_date = datetime.now(),
            updated_on = datetime.now()
        )
        customer_form_data = {
                'username': 'testuser1',
                'first_name': 'Arit',
                'last_name': 'Roy',
                'email': 'arit@gmail.com',
                'birth_date': '2000-01-01',
                'phone_number': '1234567890',
                'address': 'Badalpur',
                'city': 'City',
                'state': 'State',
                'zip_code': '12345',
                "password1":"testpassword",
                "password2":"testpassword",
        }
        
        
        form = CustomerRegistrationForm(data=customer_form_data)     
        
        form.save()
   
    
    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_get(self, mock_strip):       
        mock_strip.return_value = {'id': 5}        
        self.client.login(username = 'testuser1', password= 'testpassword')
        url = reverse('api_checkout_session', args=(self.product.id,))
        response = self.client.get(url)
        self.assertTrue(response.json(), HttpResponse)
        self.assertTrue(response.status_code, 200)
        self.assertIn("sessionId", response.json())
    