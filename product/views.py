from django.shortcuts import render, redirect
from django.views import View
from .forms import ProductForm
from django.http import HttpResponse , HttpResponseRedirect
from .models import Product, Cart, Category, SubCategory, Image
from customer.models import Customer

class ProductRegistration(View):
    def get(self, request):
        form =ProductForm
        return render(request, 'product/product.html', {"form":form})
    
    def post(self, request):
        form =ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("sucessfully Submited")
        
        
        
def add_to_cart(request):
     
    user = request.user
    product_id = request.GET.get('prod_id')
    image = Image.objects.get(id = product_id)
    print(image)
    product = Product.objects.get(image__id=product_id)  
    customer = Customer.objects.get(username = user)
    
    cart = Cart(customer=customer,product=product, image=image)
    cart.save()    
    return redirect('/product/cart')
    
def show_cart(request):
    category = Category.objects.all()
    dict1={}
    for item in category:
        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    if request.user.is_authenticated:
        user = request.user
        print(user)
        cart = Cart.objects.filter(customer = user)
        
        amount =0.0
        delivery_charges = 0.0
        total_amount = 0.0
        customer = Customer.objects.get(username = user)
        cart_product = [p for p in Cart.objects.all() if p.customer == customer]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount +=tempamount
                # print(amount) 
        
        
        
        return render(request, 'product/add_to_cart.html',{'carts':cart, 'dict1':dict1, 'amount':amount}, )