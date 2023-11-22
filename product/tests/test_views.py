from django.test import TestCase , Client
from customer.models import Customer, Vendor, User, MultipleAddress
from product.models import Product, Category, SubCategory, Wishlist, Image, Cart
from payment.models import OrderDetail
from ratting.models import Ratting
from product.forms import ProductAddForm, ProductUpdateForm, UpdateOrderForm, CancelOrderForm
from django.urls import reverse
from customer.forms import CustomerProfileForm, CustomerRegistrationForm
from product.forms import VendorRegistrationForm
import json
from django.http import JsonResponse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

    
class VendorRegistrationTestCase(TestCase):
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
        
    
    def test_vendor_registration_form_rendering(self):
        url = reverse('vendor-registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/vendor_registration_form.html')
        self.assertIsInstance(response.context['form'], VendorRegistrationForm)
    
    
    def test_vendor_registration_form_submission(self):
        # Define the URL for the view
        url = reverse('vendor-registration')  # Assuming 'vendor_registration' is the name of the URL associated with VendorRegistration view

        # Define valid test data for the POST request
        post_data = {
                'username': 'user',
                'first_name': 'Arit',
                'last_name': 'Roy',
                'email': 'arit@gmail.com',
                'birth_date': '2000-01-01',
                'phone_number': '1234567890',
                'address': 'Badalpur',
                'city': 'City',
                'state': 'State',
                'zip_code': '12345',
                'aadhar_number': '1234589012',
                'ac_number': '1293456789',
                'gst_invoice': '/home/developer/Downloads/ankit_500_11zon.jpg',
                "has_approved":False,
                "password1":"pass12345",
                "password2":"pass12345",
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/vendor_registration_form.html')
        self.assertTrue(User.objects.filter(username=post_data['username']).exists())

        
    def test_vendor_submision_invalid_forms(self):
        form = VendorRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        
    
class CartTestCase(TestCase):
    
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
        # self.rating = Ratting.objects.create(
        #     customer = self.customer,
        #     product = self.product,
        #     order = self.order,
        #     ratting = 3,
        #     comments = "kjhgfdfgh",
        #     created_at = datetime.now(),
        # )
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
        
        file_path = '/home/developer/Downloads/ankit_500_11zon.jpg'

        # Open the file and create a SimpleUploadedFile instance
        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_name = file_path.split('/')[-1]  # Extracting the file name from the path
            file = SimpleUploadedFile(file_name, file_content, content_type='image/jpg')

        vendor_form_data={
                'username': 'user12',
                'first_name': 'Arit',
                'last_name': 'Roy',
                'email': 'arit@gmail.com',
                'birth_date': '2000-01-01',
                'phone_number': '1234567890',
                'address': 'Badalpur',
                'city': 'City',
                'state': 'State',
                'zip_code': 12345,
                'aadhar_number': '1234589012',
                'ac_number': '1293456789',
                'gst_invoice': file,
                "has_approved":False,
                "password1":"pass12345",
                "password2":"pass12345",
            
        }
        form = VendorRegistrationForm(data=vendor_form_data)
        
        form.save()
        self.image = Image.objects.create(image='path/to/your/gst_invoice.jpg', product=self.product)     
        # self.cart = Cart.objects.create(customer=self.customer, product=self.product, image=self.image)
        
        
        
        
    # # add_to_cart
    def test_add_to_cart_success(self):
        self.client.login(username='testuser1', password='testpassword')
        url = reverse('add-to-cart')
        response = self.client.get(url, {'prod_id': self.product.id})      
        self.assertEqual(response.status_code,302)
        login_customer=Customer.objects.get(username = 'testuser1')    
        self.assertTrue(Cart.objects.filter(customer=login_customer, product=self.product, image=self.image).exists())
        
        
    def test_add_to_cart_product_already_in_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        Cart.objects.create(customer=self.customer, product=self.product, image=self.image)
        url = reverse('add-to-cart')
        response = self.client.get(url, {'prod_id': self.product.id})
        self.assertTrue(Cart.objects.filter(customer=self.customer, product=self.product, image=self.image).exists())

    #  show_cart
    def test_showcart_registered_user_if_not_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        url = reverse('showcart')
        response = self.client.get(url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/empty_cart.html')
        
    
    def test_showcart_registered_user_if_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username='testuser1')
        Cart.objects.create(customer=login_customer, product=self.product, image=self.image)
        url = reverse('showcart')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/add_to_cart.html')


    # add_cart
    def test_add_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username='testuser1')
        Cart.objects.create(customer=login_customer, product=self.product, image=self.image, quantity=3)
        url = reverse('addcart') 
        response = self.client.get(url, {'prod_id': self.product.id})
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {
            'quantity': 4, 
            'amount': 4000.0,   
            'totalamount': 4100.0
        })
        updated_cart_entry = Cart.objects.get(customer=login_customer, product=self.product, image=self.image)
        self.assertEqual(updated_cart_entry.quantity, 4)
        
    # # minus cart
    def test_minus_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username='testuser1')
        Cart.objects.create(customer=login_customer, product=self.product, image=self.image, quantity=1)
        url = reverse('minuscart') 
        response = self.client.get(url, {'prod_id': self.product.id})
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {
            'quantity': 1, 
            'amount': 1000.0,   
            'totalamount': 1100.0
        })
        updated_cart_entry = Cart.objects.get(customer=login_customer, product=self.product, image=self.image)
        self.assertEqual(updated_cart_entry.quantity, 1)
        
        
    # # remove cart
    def test_remove_cart(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username='testuser1')
        Cart.objects.create(customer=login_customer, product=self.product, image=self.image, quantity=3)
        url = reverse('removecart') 
        response = self.client.get(url, {'prod_id': self.product.id})
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {
            'amount': 0.0,   
            'totalamount': 0.0
        })
        
    
    # # product list   
    def test_list_product_valid_id(self):
        
        self.client.login(username='testuser1', password='testpassword')
        url = reverse('product-list',args=(self.subcategory.id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response,'product/list_product.html')
        self.assertContains(response, "Buds")
        self.assertNotContains(response, "asdf")

        
    #  product detail
    def test_product_detail_valid_product_id(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username = 'testuser1')
        Wishlist.objects.create(customer=login_customer, product=self.product, image=self.image)
        url = reverse('product-detail', args=(self.product.id, self.image.id))
        response = self.client.get(url,{"pk":self.image.id, "prod_id":self.product.id})
        self.assertTemplateUsed(response, 'product/product_detail.html')


    def test_product_detail_invalid_product_id(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username = 'testuser1')
        Wishlist.objects.create(customer=login_customer, product=self.product, image=self.image)
        url = reverse('product-detail', args=(self.image.id, 5))
        response = self.client.get(url,{"pk":self.image.id, "prod_id":self.product.id})
        self.assertEquals(response.status_code, 404)
        
    def test_product_detail_invalid_image_id(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username = 'testuser1')
        Wishlist.objects.create(customer=login_customer, product=self.product, image=self.image)
        url = reverse('product-detail', args=(5, self.product.id))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
        
    # # manage product  
    def test_manage_product(self):
        self.client.login(username='user12', password='pass12345')
        url = reverse('manage-products')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
    
    
    
    # # add products 
    def test_add_product_get(self):
        self.client.login(username='user12', password='pass12345')
        form_data = {
            'name':"accer",   
            'description':"Good laptop",
            'price':20000.90,
            'brand':"Accer",
            'color':"black",
            'category':self.category,
            'sub':self.subcategory,
        }
        form = ProductAddForm(data=form_data)
        self.assertTrue(form.is_valid())
        url = reverse("add-product")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    # def test_add_product_post(self):
    #     post_data = {
    #         'name':"Accer Black",   
    #         'description':"Good laptop for Chiled",
    #         'price':20000.00,
    #         'brand':"Accer",
    #         'color':"black",
    #         'category':self.category.id,
    #         'sub':self.subcategory.id,
    #     }
    #     self.client.login(username='user12', password='pass12345')
    #     form   = ProductAddForm(data=post_data)
    #     print(form.is_valid())
    #     self.assertTrue(form.is_valid())
    #     url = reverse("add-product")
    #     response = self.client.post(url, data=post_data)
    #     self.assertTrue(self.product.name, "Accer Black")
        
    def test_update_product(self): 
        
        update_product_data = {
            'name': 'Copy',
            'description': 'Copy Pen',
            'price' : 1000.00,
            'brand' : 'Oneplus',
            'color' : "black",
            'category': self.category.id,
            'sub': self.subcategory.id,
        }
        form = ProductUpdateForm(data=update_product_data)
        
        self.client.login(username='user12', password='pass12345')
        product = Product.objects.get(vendor__username = 'aaju5')
        url = reverse('update-product', args=(self.product.id, self.image.id))
        response = self.client.post(url, data = update_product_data)
        update_product  = Product.objects.get(id = self.product.id)   
        self.assertTrue(form.is_valid())
        self.assertTrue(update_product.description, 'Copy Pen')
        
        
    # # delete product
    def test_delete_product(self):
        prod = Product.objects.create(
            name = "Lenovo",
            description = "aaru",
            price = 1000.00,
            brand = 'Oneplus',
            color = "black",
            vendor = self.vendor,
            category = self.category,
            sub = self.subcategory)
        img = Image.objects.create(image='/gst_invoice.jpg', product=prod)     
        self.client.login(username='user12', password='pass12345')
        url = reverse('delete-product', args=(prod.id, img.id))
        response = self.client.get(url)
        self.assertFalse(Product.objects.filter(name = 'Lenovo').exists())
        self.assertTrue(Product.objects.filter(name = 'Buds').exists())
        
        
    # # view order
    def test_view_order(self):
        order = OrderDetail.objects.create(
            customer = self.customer,
            product = self.product,
            amount = 12,
            status= "Placed",
            has_paid =True,
            session_id= "123456789",
            order_date = datetime.now(),
            updated_on = datetime.now()
        )
        self.client.login(username='user12', password='pass12345')
        
        url = reverse('view-order')
        response = self.client.get(url)
    
        self.assertTemplateUsed(response, 'product/vendor_looking_order.html')
        
        self.assertIn("image", response.context)
        self.assertIn("approved", response.context)
        self.assertIn("order", response.context)
        
        
    # # update order view
    def test_update_order_status(self):
        login_customer = Customer.objects.get(username = "testuser1")
        order = OrderDetail.objects.create(
            customer = login_customer,
            product = self.product,
            amount = 12,
            status= "Placed",
            has_paid =True,
            session_id= "123456789",
            order_date = datetime.now(),
            updated_on = datetime.now()
        )
        # self.client.login(username='user12', password='pass12345')
        
        order_update_form = {
            'status':"Accepted",
        }
        
        form = UpdateOrderForm(data=order_update_form)
        url = reverse('update-status', args=(order.id,))
        response = self.client.post(url, data=order_update_form) 
        updated_order = OrderDetail.objects.get(customer = login_customer)
        self.assertEquals(updated_order.status,"Accepted")
        self.assertEquals(response.status_code, 302)
    
    
    # delete order 
    def test_delete_order(self):
        order = OrderDetail.objects.create(
            customer = self.customer,
            product = self.product,
            amount = 12,
            status= "Placed",
            has_paid =True,
            session_id= "123456789",
            order_date = datetime.now(),
            updated_on = datetime.now()
        )
        self.assertTrue(OrderDetail.objects.filter(customer=self.customer).exists())     
        url = reverse('delete-status', args= (order.id,))
        response  = self.client.get(url)
        self.assertTrue(OrderDetail.objects.filter(customer=self.customer).exists())
        
        
    # TrackDetail
    
    def test_track_detail_view(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username = 'testuser1')
        Ratting.objects.create(
            customer = login_customer,
            product = self.product,
            order = self.order,
            ratting = 2,
            comments = "kjhgfdfgh",
            created_at = datetime.now(),
        )
        url = reverse('track-product', args=(self.image.id,self.order.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)       
        self.assertEqual(response.context['image'], self.image)
        self.assertEqual(response.context['order'], self.order)
        self.assertEqual(response.context['rattings'].count(), 1) 
        self.assertEqual(response.context['dict1'][self.category.name].count(), 1)   
        self.assertTemplateUsed(response, 'product/track_product.html')
    
    
    # # orderhistory
    def test_order_history(self):
        self.client.login(username='testuser1', password='testpassword')
        login_customer = Customer.objects.get(username = 'testuser1')
        order = OrderDetail.objects.create(
            customer = login_customer,
            product = self.product,
            amount = 12,
            status= "Placed",
            has_paid =True,
            session_id= "123456789",
            order_date = datetime.now(),
            updated_on = datetime.now()
        )
    
        url = reverse('history')
        response = self.client.get(url)
        self.assertTrue(response.context['object_list'],order)
        self.assertTrue(response.context['object_list'].count(), 1)
        self.assertTemplateUsed(response, 'product/order_history.html')
        
        
    # # cancel order
    
    def test_cancel_order_get(self):
        
        cancel_order_form = {
            'reasion':"PRA.",
        }
        form = CancelOrderForm(data=cancel_order_form)     
        self.client.login(username='testuser1', password='testpassword')
        url = reverse('order-cancel', args=[self.image.product.id, self.image.id, self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['image'], self.image)
        self.assertIsInstance(response.context['form'], CancelOrderForm)
        self.assertTemplateUsed(response, 'product/order_cancel.html')
        
        
    def test_cancel_order_with_invalid_id(self):     
        url = reverse('order-cancel', args=[self.image.product.id, 5, self.order.id])
        response = self.client.get(url)
        self.assertTrue(response, 404)
        # self.assertTemplateUsed(response, 'product/order_cancel.html')

    
    def test_cancel_order_post(self):
        cancel_order_form = {
            'reasion':"PRA.",
        }
        form = CancelOrderForm(data=cancel_order_form)   
        url = reverse('order-cancel', args=[self.image.product.id, self.image.id, self.order.id])
        response = self.client.post(url, data=cancel_order_form)
        self.assertTrue(response, 200)
        self.assertFalse(response.context['order'], False)
        self.assertTemplateUsed(response, 'product/order_cancel_successfully.html')


    
        