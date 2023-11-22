
from django.http import HttpResponse, JsonResponse
from product.models import Product
from customer.models import Customer
from .models import Ratting
from payment.models import OrderDetail
# Create your views here.
def ratting(request):
    if request.method=="POST":          
        product_id = request.POST.get("prod_id")
        comment = request.POST.get('comment')
        rating = request.POST.get("value_of_star")
        order_id = request.POST.get("order_id")
        order = OrderDetail.objects.get(id=order_id)
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(username=request.user)
        Ratting.objects.create(customer=customer, product=product, comments=comment,ratting=rating, order=order)
        return JsonResponse({"response":"successfull"})
    return  HttpResponse("Fail")
