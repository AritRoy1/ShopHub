from django.urls import path
from product import views
urlpatterns = [
    
    
    path("registration/", views.ProductRegistration.as_view(), name="product-registration"),
    path('add-to-cart/', views.add_to_cart, name = 'add-to-cart'),
    path('cart/', views.show_cart, name = 'showcart'),
    
        
]