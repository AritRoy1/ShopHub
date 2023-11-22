from django.test import TestCase, client
from customer.forms import CustomerRegistrationForm
from customer.models import Customer
from django.urls import reverse
class LoginTest(TestCase):
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
    
    def test_login_post(self):
        self.client.login(username = 'testuser1', password = "testpassword")
        url = reverse('login')
        data = {
            'username' : 'testuser1',
            'password': 'testpassword'
        }
        
        # login with valid uername password    
        response = self.client.post(url,data=data)
        self.assertEquals(response.status_code,302)
        self.assertRedirects(response, '/')
       
       # user log in with invalid username
        response =  self.client.post(url,{"username":'test','password':'testpassword'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'customer/login.html')
        self.assertEquals(response.context['message'],'username password not match')
        
        # user log in with invalid  password
        response =  self.client.post(url,{"username":'testuser1','password':'password'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'customer/login.html')
        self.assertEquals(response.context['message'],'username password not match')

        # user log in with invalid username password
        response =  self.client.post(url,{"username":'user1','password':'password'})
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'customer/login.html')
        self.assertEquals(response.context['message'],'username password not match')