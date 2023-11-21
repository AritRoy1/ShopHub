from django.test import TestCase , Client
from customer.models import Customer, Vendor, User, MultipleAddress
from product.models import Product, Category, SubCategory, Wishlist, Image
from django.urls import reverse
from customer.forms import CustomerProfileForm, CustomerRegistrationForm
import json
from django.http import JsonResponse
# Create your tests here.

class CustomerTestCase(TestCase):
    
    def setUp(self):
       self.user = User.objects.create_user(username='user', password='password')
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
    def test_home_view(self):
        
        client = Client()
        response = client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/home.html')
        
    def test_customer_registration_get(self):
        client = Client()
        response = client.get(reverse("customer-registration"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_registration.html')
        
        
    def test_customer_registration_post(self):
        client = Client() 
        post_data = {
            'username': "aaju1",
            "first_name": "ajad",
            "last_name": 'sarkar',
            'email': "jhgfds@gmail.com",
            'birth_date': "19/5/2001",
            'phone_number': 76174322345120,
            'address': "bhopal",
            'city': 'Indore',
            'state': "M.P",
            'zip_code': 460440     
        }
        
        response = client.post(reverse("customer-registration"), data=post_data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.status_code in [200,302])  
        self.assertTemplateUsed(response, 'customer/customer_registration.html')
        
class LoginTestCase(TestCase):
    
    def test_get_login_view(self):
        url = reverse('login')  
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/login.html')
    
    def test_post_login_view(self):
        User.objects.create_user(username = "AritRoy1", password = "qwertyuiop")
        url = reverse('login')  
        client = Client()
        response = client.post(url, {'username': 'AritRoy1', 'password': 'qwertyuiop'})

        # Check if the response redirects to the correct URL after successful login
        self.assertRedirects(response, '/')
        
        
    def test_post_login_view_failure(self):
        url = reverse('login')  
        response = self.client.post(url, {'username': 'user', 'password': 'password'})
        self.assertTemplateUsed(response, 'customer/login.html')
        self.assertContains(response, 'username password not match')

    
    # custmer profile test
    def test_get_customer_profile(self):  
        url = reverse('profile')
        response = self.client.get(url) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_profile.html')

    def test_post_customer_profile(self):
        self.client.login(username='user', password='password')
        url = reverse('profile')
        client = Client() 
        post_data = {'first_name':"A",'last_name':"B",'email':"jhgfsdfgh@gmail.com",
                                     'birth_date':"2000-12-23", 'phone_number':"99999999456",
                                     'city':'4567','state':"AS","address":"jhgfdfg"}
        
        response = self.client.post(url, data=post_data)
        form  = CustomerProfileForm(data=post_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_profile.html')

        
        # error
        # self.assertRedirects(response, '/customer-profile/')
        
    

class Address(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {
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
        
        form = CustomerRegistrationForm(data=form_data)
        
        form.save()
        
       
    def test_add_address_get(self):
        url = reverse('add-address')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_add_address.html')
        

    def test_add_address_post(self):
        self.client.login(username='testuser1', password='testpassword')
        
        post_data = {
            'name': 'Pankaj udas',
            'phone_number': '1234567890',
            'pincode': 460440,
            'locality': 'Indian',
            'address': 'Chopna oh nghjg hgj',
            'city': 'Betul',
            'state': 'AS',
            'landmark': 'lkjhg',          
        }
        
        url = reverse('add-address')
        response = self.client.post(url,post_data)  
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,"/address/")

    def test_delete_address(self):
        mul = MultipleAddress.objects.create(
            name= 'Pankaj udas',
            phone_number= '1234567890',
            pincode= 460440,
            locality= 'Indian',
            address= 'Chopna oh nghjg hgj',
            city= 'Betul',
            state= 'AS',
            landmark= 'lkjhg',
        )
        url =reverse("delete-address", args=(1,))
        response = self.client.delete(url, json.dumps({'id':1}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,"/address/")
        
class WishlistTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username="user", password="password")
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
        form_data = {
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
        
        form = CustomerRegistrationForm(data=form_data)     
        form.save()     
        self.image = Image.objects.create(image='path/to/your/gst_invoice.jpg', product=self.product)     
        self.wishlist_item = Wishlist.objects.create(customer=self.customer, product=self.product, image=self.image)
        self.client = Client()
        
    def test_wishlist_view(self):
        url = reverse('wishlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)    
        self.assertTemplateUsed(response, 'customer/wishlist.html')    


    def test_delete_from_wishlist(self):
        self.client.login(username = 'testuser1', password='testpassword')    
        url = reverse('remove_from_wishlist', args=[self.image.id])     
        response = self.client.get(url)
        print("kjhgf")
        print(response.json())
        self.assertIsInstance(response, JsonResponse)
        self.assertEquals(response.json(), {'message':'Item was not in the wishlist'})
        
    def test_delete_from_wishlist_not(self):
        self.client.login(username='testuser1', password='testpassword')
        self.wishlist_item.delete()
        url = reverse('remove_from_wishlist', args=[self.image.id])
        response = self.client.get(url)
        self.assertEquals(response.json(), {'message':'Item was not in the wishlist'})
        
        
    def test_delete_from_wishlist_id_notexist(self):
        self.client.login(username='testuser1', password='testpassword')
        self.wishlist_item.delete()
        url = reverse('remove_from_wishlist', args=[5,])
        response = self.client.get(url)
        self.assertEqual(response.status_code , 404)
        