
from django.http import HttpResponse, JsonResponse
from product.models import Product
from customer.models import Customer
from .models import Ratting
# Create your views here.
def ratting(request):
    print("ratting")
    if request.method=="POST":          
        product_id = request.POST.get("prod_id")
        comment = request.POST.get('comment')
        rating = request.POST.get("value_of_star")
        product = Product.objects.get(id=product_id)
        customer = Customer.objects.get(username=request.user)
        Ratting.objects.create(customer=customer, product=product, comments=comment,ratting=rating)
        return JsonResponse({"response":"successfull"})
    return  HttpResponse("success")
