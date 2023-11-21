from django.test import SimpleTestCase
from django.urls import reverse, resolve
from product.views import VendorRegistration, addProducts, vendor_pannel, add_to_cart, view_Order,graph_Bar,search ,show_cart, ProductList, ProductDetail, TrackDetail,CancelOrder, OrderHistoryView
class ProductUrlTest(SimpleTestCase):
    
    def test_vendor_registration_url(self):
        url = reverse('vendor-registration')
        self.assertEqual(resolve(url).func, VendorRegistration)
    
    def test_vendor_pannel_url(self):
        url = reverse('vendor-pannel')
        self.assertEqual(resolve(url).func, vendor_pannel)
    
    def test_add_to_cart_url(self):
        url = reverse('add-to-cart')
        self.assertEqual(resolve(url).func, add_to_cart)
    
    def test_show_cart_url(self):
        url = reverse('showcart')
        self.assertEqual(resolve(url).func, show_cart)
        
    def test_list_of_product_url(self):
        url = reverse('product-list', args=(1,))
        self.assertEqual(resolve(url).func.view_class, ProductList)
        
    def test_product_detail_url(self):
        url = reverse('product-detail', args=(1,2))
        self.assertEqual(resolve(url).func.view_class, ProductDetail)
    
    def test_vendor_add_product_url(self):
        url = reverse('add-product')
        self.assertEqual(resolve(url).func, addProducts)
        
    def test_vendor_view_order_url(self):
        url = reverse('view-order')
        self.assertEqual(resolve(url).func, view_Order)
    
    def test_graph_bar_url(self):
        url = reverse('graph-bar')
        self.assertEqual(resolve(url).func, graph_Bar)   
    
    def test_search_bar_url(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search)   
    
    def test_track_detail_url(self):
        url = reverse('track-product', args=(1,2))
        self.assertEqual(resolve(url).func.view_class, TrackDetail)   
    
    def test_order_history_url(self):
        url = reverse('history')
        self.assertEqual(resolve(url).func.view_class,OrderHistoryView)   
    
    def test_cancel_order_url(self):
        url = reverse('order-cancel', args=(1,2,3))
        self.assertEqual(resolve(url).func.view_class, CancelOrder)