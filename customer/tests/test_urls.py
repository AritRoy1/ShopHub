from django.test import SimpleTestCase
from django.urls import reverse, resolve
from customer.views import home, Login, logout_view, CustomerProfile, AddAddress, wishlist, remove_from_wishlist
from product.models  import Product


class TestUrls(SimpleTestCase): 
    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)
    
    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, Login)
    
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)
    
    def test_customer_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, CustomerProfile)

    def test_add_addresss_url(self):
        url = reverse('add-address')
        self.assertEquals(resolve(url).func.view_class, AddAddress)

    def test_wishlist_url(self):
        url = reverse('wishlist')
        self.assertEquals(resolve(url).func, wishlist)
    
    def test_remove_wishlist_url(self):    
        url = reverse('remove_from_wishlist', args=(1,))
        self.assertEquals(resolve(url).func, remove_from_wishlist)