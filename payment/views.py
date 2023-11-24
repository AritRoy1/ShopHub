from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product, OrderDetail
from django.views.generic import TemplateView
from django.views import View
import stripe
from django.conf import settings
from ShopHub import settings as shop_settings
from django.views.decorators.csrf import csrf_exempt
import json
from customer.models import Customer
from django.core.mail import send_mail
from django.urls import reverse



# Create your views here.

# create a checkout session for payment
@csrf_exempt
def create_checkout_session(request, id):
    # request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)
    customer  = get_object_or_404(Customer, username=request.user)    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price*100),
                },
                'quantity': 1,
            }
        ],
        metadata = {"product_id":id},
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )
    
    order = OrderDetail() 
    print(checkout_session['id'])
    order.customer = customer
    order.product = product
    order.session_id = checkout_session['id']  
    order.amount = int(product.price)      
    order.save()
    return JsonResponse({'sessionId': checkout_session['id'] })


class PaymentSuccessView(TemplateView):
    # render sucess page  after payment successfully done. 
    template_name = "payments/payment_success.html"
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class PaymentFailedView(TemplateView):
    # render Failed page  after payment failed.   
    template_name = "payments/payment_failed.html"

    
## Webhook payment
endpoint_secret = 'whsec_589a26ad9858647a340c08dd70f384294d7dc130a853e12fd2d939fa42e5de05'
stripe.api_key = shop_settings.STRIPE_API_KEY

@csrf_exempt
def my_webhook_view(request):
  payload = request.body 
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Save an order in your database, marked as 'awaiting payment'
    create_order(request, session)

    if session.payment_status == "paid":
      # Fulfill the purchase
      fulfill_order(session)

  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']

    # Fulfill the purchase
    fulfill_order(session)

  elif event['type'] == 'checkout.session.async_payment_failed':
    session = event['data']['object']

    # Send an email to the customer asking them to retry their order
    email_customer_about_failed_payment(session)
    
  # Passed signature verification
  return HttpResponse(status=200)


def create_order(request,session):
        print(session['customer_details']['email'])    
        order = get_object_or_404(OrderDetail,session_id = session['id'])


# send email to customer after payment successfully done.             
def fulfill_order(session):
        order = get_object_or_404(OrderDetail,session_id = session['id'])       
        order.has_paid = True
        order.save()      
        subject = 'Payment Successfull'
        message = f'Your Order is Conformed, Your order will reach soon, You can track your Order..'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [session['customer_details']['email']]
        send_mail( subject, message, email_from, recipient_list )


# send email to customer for payment is  Not successfull  
def email_customer_about_failed_payment(session): 
    subject = 'Payment Faild'
    message = f'Your Order is Not Conformed, Due To Payment Falid..'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [session['customer_details']['email'] ]
    send_mail( subject, message, email_from, recipient_list ) 

