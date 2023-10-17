from django.urls import path
from customer import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm
urlpatterns = [
    
    path('home/',views.home, name="home"),
    
    
    path('customer/registration/', views.CustomerRegistration, name='customer-registration'),
    path('vendor/registration/', views.VendorRegistration, name = 'vendor-registration'),
    
    # path('accounts/login', auth_view.LoginView.as_view(template_name="customer/login.html", 
    #         authentication_form=LoginForm), name='login')
    path('login/', views.Login.as_view(), name= 'login'),
    path('logout/', views.logout_view, name='logout'),
    path('electronics-detail/', views.ProductDetail.as_view() ,name='Electronics'),
    path('product-list/<int:pk>', views.ProductList.as_view(), name="product-list"),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('cart/', views.Cart.as_view(), name = 'cart')
    
    
        
]