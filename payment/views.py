from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Product, OrderDetail
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.views import View
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from product.models import Image
from customer.models import Customer
from django.core.mail import send_mail

# Create your views here.

@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)
    customer  = get_object_or_404(Customer, username=request.user)

    print(id)
    print("jai")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(stripe.api_key)
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
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )
    
    print("checout session")
    
    print()
    print(checkout_session)

    order = OrderDetail()
    # order.customer_email = request_data['email']
    order.customer = customer
    order.product = product
    order.session_id = checkout_session['id']  
    order.amount = int(product.price)  
    order.save()
    
    print("lkjhgfgh")

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        print('serr',session_id)
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        print('session', session)

        order = get_object_or_404(OrderDetail,session_id = session.id)
        order.has_paid = True
        order.save()
        subject = 'Payment Successfull'
        message = f'Your Order is Conformed, Your order will reach soon, You can track your Order..'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['arit2000roy@gmail.com' ]
        send_mail( subject, message, email_from, recipient_list )

        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    
    template_name = "payments/payment_failed.html"

class OrderHistoryView(View):
    def get(self, request):
        print(request.user)
        model = OrderDetail.objects.filter(customer__username=request.user)
        return render(request, 'payments/order_history.html', {"object_list":model})
           
    # model = OrderDetail.objects.get()
    # template_name = "payments/order_history.html"
    
class TrackDetailView(DetailView):
    
   
    model = Product
    template_name = "payments/track_detail.html"
    def get_context_data(self, **kwargs,):
        pk=self.kwargs.get('pk')
        context = super(TrackDetailView, self).get_context_data(**kwargs)
        context['image'] = Image.objects.get(product__id = pk)
        context['order'] = OrderDetail.objects.get(product__id = pk)
        
        
        return context
    