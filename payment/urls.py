from django.urls import path
from .views import *

urlpatterns = [
  
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryView.as_view(), name='history'),
    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
    path('webhook',my_webhook_view, name="webhook"),
    path('track-detail/<pk>/<item_id>', TrackDetail.as_view(), name = 'track-product'),
    path('order-cancel/<product_id>/<image_id>/<order_id>/', CancelOrder.as_view(), name='order-cancel')
]