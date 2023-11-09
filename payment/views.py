from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseNotFound, JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Product, OrderDetail
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.views import View
import stripe
from django.conf import settings
from ShopHub import settings as shop_settings
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import Image
from customer.models import Customer
from ratting.models import Ratting
from django.core.mail import send_mail
from payment.forms import CancelOrderForm

# Create your views here.

@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)
    customer  = get_object_or_404(Customer, username=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
   
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email = request_data['email'],
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
    # order.customer_email = request_data['email']
    order.customer = customer
    order.product = product
    order.session_id = checkout_session['id']  
    order.amount = int(product.price)  
    order.save()
    

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    print("payment Success View")
    
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        # session_id = request.GET.get('session_id')
  
        # if session_id is None:
        #     return HttpResponseNotFound()
        
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        # session = stripe.checkout.Session.retrieve(session_id)
        # order = get_object_or_404(OrderDetail,session_id = session.id)
        # order.has_paid = True
        # order.save()
        
        # subject = 'Payment Successfull'
        # message = f'Your Order is Conformed, Your order will reach soon, You can track your Order..'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['arit2000roy@gmail.com' ]
        # send_mail( subject, message, email_from, recipient_list )

        return render(request,self.template_name)

class PaymentFailedView(TemplateView):
    
    template_name = "payments/payment_failed.html"

class OrderHistoryView(View):
    def get(self, request):
        print(request.user)
        model = OrderDetail.objects.filter(customer__username=request.user)
        return render(request, 'payments/order_history.html', {"object_list":model})
           
    # model = OrderDetail.objects.get()
    # template_name = "payments/order_history.html"
    
class TrackDetail(DetailView):
    
   
    model = Product
    template_name = "payments/track_detail.html"
    def get_context_data(self, **kwargs,):
        pk=self.kwargs.get('pk')
        item_id = self.kwargs.get('item_id')
        print(item_id)
        context = super(TrackDetail, self).get_context_data(**kwargs)
        context['image'] = Image.objects.get(product__id = pk)
        # context['order'] = OrderDetail.objects.filter(product__id = pk,customer=self.request.user)     
        context['order'] = OrderDetail.objects.get(id=item_id)     
        context['rattings'] = Ratting.objects.filter(customer=self.request.user, product__id=pk, order__id=item_id)

        return context
    
## Webhook

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

    # Check if the order is already paid (for example, from a card payment)
    #
    # A delayed notification payment will have an `unpaid` status, as
    # you're still waiting for funds to be transferred from the customer's
    # account.
    
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


def fulfill_order(session):
        print(session['customer_details']['email'])
        order = get_object_or_404(OrderDetail,session_id = session['id'])       
        order.has_paid = True
        order.save()
        
        # send email to customer for payment successfull             
        subject = 'Payment Successfull'
        message = f'Your Order is Conformed, Your order will reach soon, You can track your Order..'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [session['customer_details']['email']]
        send_mail( subject, message, email_from, recipient_list )



def email_customer_about_failed_payment(session):
    
     # send email to customer for payment is  Not successfull  
    subject = 'Payment Faild'
    message = f'Your Order is Not Conformed, Due To Payment Falid..'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [session['customer_details']['email'] ]
    send_mail( subject, message, email_from, recipient_list ) 
    print("Emailing customer")



class CancelOrder(View):
    def get(self, request, product_id, image_id, order_id ):
      image = Image.objects.get(pk=image_id)  
      form = CancelOrderForm()
      return render(request, 'payments/order_cancel.html', {"form":form, "image":image})
      
    def post(self, request, product_id, image_id, order_id):
      
      form = CancelOrderForm(request.POST)
      order = OrderDetail.objects.get(id=order_id)
      if form.is_valid():  
        order.has_paid=False
        order.save()  
        subject = 'Order Cancel'
        message = f'Your order has been cancel .. Your Paymnet will send to your account within 5 to 6 working day'
        email_from = settings.EMAIL_HOST_USER
        # recipient_list = [session['customer_details']['email'] ]
        recipient_list = ['arit2000roy@gmail.com' ]
        
        send_mail( subject, message, email_from, recipient_list ) 
        print("Emailing customer")
        
    
        return render(request,'payments/order_cancel_successfilly.html')