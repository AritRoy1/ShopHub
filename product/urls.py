from django.urls import path
from product import views
urlpatterns = [
    
    
    path('vendor-registration/', views.VendorRegistration, name = 'vendor-registration'),
    path('vendor-pannel/', views.vendor_pannel, name = 'vendor-pannel'),
    path('manage-product/', views.manage_products, name='manage-products'),
    path('delete-product/<int:pk>/<int:val>/', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>/<int:val>/', views.update_product_view,name='update-product'),
    path('add-product', views.addProducts, name='add-product'),
    path('view-order/', views.view_Order, name = "view-order"),
    path('update-status/<pk>/', views.update_order_status, name='update-status'),
    path('delete-status/<pk>/', views.delete_order_status, name='delete-status'),
    path('product-list/<int:pk>', views.ProductList.as_view(), name="product-list"),
    path('product-detail/<int:pk>/<int:prod_id>', views.ProductDetail.as_view(), name='product-detail'),
    path('track-detail/<pk>/<item_id>', views.TrackDetail.as_view(), name = 'track-product'),
    path('history/', views.OrderHistoryView.as_view(), name='history'),
    path('order-cancel/<product_id>/<image_id>/<order_id>/', views.CancelOrder.as_view(), name='order-cancel'),


    
    
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('show-cart/', views.show_cart, name = 'showcart'),
    path('addcart/', views.add_cart, name='addcart'),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('search/', views.search, name = 'search'),
  
    
]