from django.urls import path
from product import views
urlpatterns = [
    
    
    path('vendor-registration/', views.VendorRegistration, name = 'vendor-registration'),
    path("registration/", views.ProductRegistration.as_view(), name="product-registration"),
    path('vendor-pannel/', views.vendor_pannel, name = 'vendor-pannel'),
    path('manage-product/', views.manage_products, name='manage-products'),
    path('delete-product/<int:pk>/<int:val>/', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>/<int:val>/', views.update_product_view,name='update-product'),
    path('add-product', views.addProducts, name='add-product'),
    path('view-order/', views.view_Order, name = "view-order"),
    path('update-status/<pk>/', views.update_order_status, name='update-status'),
    path('delete-status/<pk>/', views.delete_order_status, name='delete-status'),
    
    
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('show-cart/', views.show_cart, name = 'showcart'),
    path('addcart/', views.add_cart, name='addcart'),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('search/', views.search, name = 'search'),
    path("wishlist/", views.wishlist, name='wishlist'),
    
]