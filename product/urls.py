from django.urls import path
from product import views
urlpatterns = [
    
    
    path("registration/", views.ProductRegistration.as_view(), name="product-registration")
    
        
]