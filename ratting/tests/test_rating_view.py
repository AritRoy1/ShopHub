from django.test import TestCase , Client
from product.models import Product, SubCategory, Category, Image
from customer.models import Customer, User, Vendor
from customer.forms import CustomerRegistrationForm
from ratting.models import Ratting
from payment.models import OrderDetail
from datetime import datetime
from django.urls import reverse
from django.http import JsonResponse, HttpResponse


# Create your views here.

class RatingTestCase(TestCase):
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
            price = 12345.89,
            brand = 'Oneplus',
            color = "black",
            vendor = self.vendor,
            category = self.category,
            sub = self.subcategory
        )
        
        self.image = Image.objects.create(image='path/to/your/gst_invoice.jpg', product=self.product)     
        
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
        self.rating = Ratting.objects.create(
            customer = self.customer,
            product = self.product,
            order = self.order,
            ratting = 3,
            comments = "kjhgfdfgh",
            created_at = datetime.now(),
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
    
    # create ratting with valid id 
    def test_ratting_test_post(self):
        self.client.login(username = 'testuser1', password="testpassword")
        url = reverse('ratting')
        data = {
            "prod_id":self.product.id,
            "comment":"very nice",
            "value_of_star":4,
            "order_id":self.order.id,    
        }
        response = self.client.post(url,data=data)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIsInstance(response, HttpResponse)
        
        
    def test_rating_invalid_id(self):
        self.client.login(username = 'testuser1', password="testpassword")
        url = reverse('ratting')
        data = {
            "prod_id":3,
            "comment":"very nice",
            "value_of_star":4,
            "order_id":4,    
        }
        response = self.client.get(url,data=data)
        print(response)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        