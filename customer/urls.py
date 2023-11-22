from django.urls import path
from customer import views
from django.contrib.auth.views import (
      
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    
    path('',views.home, name="home"),
    path('customer/registration/', views.CustomerRegistration, name='customer-registration'),    
    path('login/', views.Login.as_view(), name= 'login'),
    path('logout/', views.logout_view, name='logout'),
    
    # reset password 
    path('password-reset/', PasswordResetView.as_view(template_name='customer/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='customer/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='customer/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='customer/password_reset_complete.html'),name='password_reset_complete'), 

    path("show-more-review/", views.show_more_review, name="show-review"),
    path("customer-profile/", views.CustomerProfile.as_view(), name = "profile"),
    path("address/", views.show_address, name = 'address'),
    path("add-address/", views.AddAddress.as_view(), name = 'add-address'),

    # wishlist 
    path("delete-address/<int:pk>/", views.delete_address, name="delete-address"),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path("wishlist/", views.wishlist, name='wishlist'),
    path('demo/', views.demo, name="demo")
    
    
]
