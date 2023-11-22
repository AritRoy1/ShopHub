# from django.test import TestCase, SimpleTestCase
# from product.forms import ProductUpdateForm, VendorRegistrationForm, ProductAddForm, UpdateOrderForm
# from product.models import Category, SubCategory, Product
# from customer.models import Vendor , Customer
# from datetime import datetime

# class ProductFormCase(TestCase):
#     def test_product_update_form_valid_data(self):
#         form_data =  {
#             'name':"panthor",
#             'description': "kjhgfd",
#             'price':122222,
#             "brand": "lenovo",
#             'color':"blue",
#         }
#         form = ProductUpdateForm(data=form_data)
#         self.assertTrue(form.is_valid())
        
#     def test_product_update_form_invalid_data(self):
        
#         form = ProductUpdateForm(data={})
#         self.assertFalse(form.is_valid())
        
#     def test_vendor_registration_valid_data(self):
#         form_data = {
#                 'username': 'user12',
#                 'first_name': 'Arit',
#                 'last_name': 'Roy',
#                 'email': 'arit@gmail.com',
#                 'birth_date': '2000-01-01',
#                 'phone_number': '1234567890',
#                 'address': 'Badalpur',
#                 'city': 'City',
#                 'state': 'State',
#                 'zip_code': '12345',
#                 'aadhar_number': '1234589012',
#                 'ac_number': '1293456789',
#                 'gst_invoice': '/home/developer/Downloads/ankit_500_11zon.jpg',
#                 "has_approved":False,
#                 "password1":"pass12345",
#                 "password2":"pass12345",
#             }
        
#         form=VendorRegistrationForm(data=form_data)
#         self.assertTrue(form.is_valid())
        
#     def test_vendor_registration_invalid_data(self):
#         form=VendorRegistrationForm(data={})
#         self.assertFalse(form.is_valid())
  
  
# class ProductForm(TestCase): 
#     def setUp(self):
#         self.customer = Customer.objects.create(
#             username= "aaju10",
#             first_name ="ajad",
#             last_name= 'sarkar',
#             email ="jhgfds@gmail.com",
#             birth_date= "2001-9-5",
#             phone_number= "7617354120",
#             address ="bhopal",
#             city ='Indore',
#             state ="M.P",
#             zip_code= 460440 
#         )
        
#         self.vendor = Vendor.objects.create(
#                 username= "aaju5",
#                 first_name ="ajad",
#                 last_name= 'sarkar',
#                 email ="jhgfds@gmail.com",
#                 birth_date= "2001-9-5",
#                 phone_number= "7617354120",
#                 address ="bhopal",
#                 city ='Indore',
#                 state ="M.P",
#                 zip_code= 460440 ,
#                 aadhar_number=87654,
#                 ac_number=987654,
#                 gst_invoice = 'path/to/your/gst_invoice.jpg',
#                 has_approved = True
#             )  
        
#         self.category = Category.objects.create(
#                 name  = "Electronics",
#                 vendor = self.vendor
#             )
    
#         self.subcategory = SubCategory.objects.create(
#             name = "laptop",
#             category = self.category
#             ) 
        
#         self.product = Product.objects.create(
#             name = "Buds",
#             description = "kjhgfddfgh",
#             price = 12345.89,
#             brand = 'Oneplus',
#             color = "black",
#             vendor = self.vendor,
#             category = self.category,
#             sub = self.subcategory
#         )
        
        
#     def test_add_product(self):
        
#         form_data = {
#             'name':"accer",   
#             'description':"Good laptop",
#             'price':20000.90,
#             'brand':"Accer",
#             'color':"black",
#             'category':self.category,
#             'sub':self.subcategory,
#         }
        
#         form=ProductAddForm(data=form_data)
#         self.assertTrue(form.is_valid())
        
#     def  test_add_product_invalid_data(self):
#         form=ProductAddForm(data={})
#         self.assertFalse(form.is_valid())


#     def test_update_order_form_valid(self):
#         form_data = {
#             "status":"Placed",
#             "customer":self.customer,
#             'product':self.product,
#             'amount':123454,
#             "has_paid":False,
#             "session_id":"987654567",
#             'order_date':datetime.now(),
#             "updated_on":datetime.now(),
#         }

#         form=UpdateOrderForm(data=form_data)
#         self.assertTrue(form.is_valid())
    
#     def test_update_order_form_invalid(self):
        
#         form=UpdateOrderForm(data={})
#         self.assertFalse(form.is_valid())