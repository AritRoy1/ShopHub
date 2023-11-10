from django.urls import path
from customer import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from django.contrib.auth.views import (
    
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    
    path('home/',views.home, name="home"),
    
    
    path('customer/registration/', views.CustomerRegistration, name='customer-registration'),
    # path('vendor/registration/', views.VendorRegistration, name = 'vendor-registration'),
    
    # path('accounts/login', auth_view.LoginView.as_view(template_name="customer/login.html", 
    #         authentication_form=LoginForm), name='login')
    path('login/', views.Login.as_view(), name= 'login'),
    path('logout/', views.logout_view, name='logout'),
    
    # reset password 
    
    path('password-reset/', PasswordResetView.as_view(template_name='customer/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='customer/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='customer/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='customer/password_reset_complete.html'),name='password_reset_complete'),

    path('electronics-detail/', views.ProductDetail.as_view() ,name='Electronics'),
    path('product-list/<int:pk>', views.ProductList.as_view(), name="product-list"),
    path('product-detail/<int:pk>/<int:prod_id>', views.ProductDetail.as_view(), name='product-detail'),
    path("show-more-review/", views.show_more_review, name="show-review"),
    path("profile/", views.CustomerProfile.as_view(), name="profile"),
    path("address/", views.address, name = 'address'),
    path("add-address/", views.AddAddress.as_view(), name = 'add-address'),
    path("delete-address/<int:pk>/", views.delete_address, name="delete-address"),
    # path('remove_wishlist_data/', views.remove_wishlist_data, name = "remove-wishlist"),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    
    
   path("demo/", views.demo, name='demo'),
    
        
]
