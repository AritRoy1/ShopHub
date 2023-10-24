from django.shortcuts import render, redirect
from django.views import View
from .forms import ProductForm
from django.http import HttpResponse , HttpResponseRedirect
from .models import Product, Cart, Category, SubCategory, Image
from customer.models import Customer
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery
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
        delivery_charges = 100
        total_amount = 0.0
        customer = Customer.objects.get(username = user)
        cart_product = [p for p in Cart.objects.all() if p.customer == customer]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount +=tempamount
                total_amount = amount+delivery_charges
                # print(amount)   
        
            return render(request, 'product/add_to_cart.html',{'carts':cart, 'dict1':dict1, 'amount':amount, 'totalamount':total_amount}, )
        else:
            return render(request, "product/cart.html")
    
def add_cart(request):
    
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        
        user = request.user
        print(user)
        
        customer = Customer.objects.get(username = user)
        print(customer)
        
        
        
        c = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
        print("c",c)
        print(c.quantity)
        
        c.quantity+=1
        c.save()
        delivery_charges = 100
        amount =0.0
        total_amount=0.0
        
        
        cart_product = [p for p in Cart.objects.all() if p.customer == customer]
        for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                print("q",p.quantity)
                print("price",p.product.price )
                print(tempamount)
                amount +=tempamount
                total_amount = amount+delivery_charges
                
                print("amount",amount)
    data = {
        "quantity":c.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)
        
def minus_cart(request):
    
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        
        user = request.user
        print(user)
        
        customer = Customer.objects.get(username = user)
        print(customer)
        
        
        
        c = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
        print("c",c)
        print(c.quantity)
        
        c.quantity-=1
        c.save()
        delivery_charges = 100
        amount =0.0
        total_amount=0.0
        
        
        cart_product = [p for p in Cart.objects.all() if p.customer == customer]
        for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                print("q",p.quantity)
                print("price",p.product.price )
                print(tempamount)
                amount +=tempamount
                total_amount = amount+delivery_charges
                
                print("amount",amount)
    data = {
        "quantity":c.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)

       
def remove_cart(request):
    
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        
        user = request.user
        print(user)
        
        customer = Customer.objects.get(username = user)
        print(customer)
        
        
        
        c = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
        print("c",c)
        print(c.quantity)
        
        c.delete()
        delivery_charges = 100
        amount =0.0
        total_amount=0.0
        
        
        cart_product = [p for p in Cart.objects.all() if p.customer == customer]
        for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                print("q",p.quantity)
                print("price",p.product.price )
                print(tempamount)
                amount +=tempamount
                total_amount = amount+delivery_charges
                
                print("amount",amount)
    data = {
        
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)

def search(request):
    dict1={}
    category = Category.objects.all()
    for item in category:
        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    if request.method=='GET':
        print("GET1")
        
        if 'search' in request.GET:
            print("GET2")
            print("----------------")
            var = request.GET.get('search')
            var1 = request.GET.get('test')
            
           
            
            print("var",var)
            print("var1",var1)
           
            
            # print(type(var2))
            
            brand_item = Product.objects.filter(sub__name__icontains=var).distinct("brand",'color')
            # print(product)
            # color = Product.objects.filter(sub__name__icontains)
            
            
            # filter by price
            if var1=='1':
                image  = Image.objects.filter(Q(product__sub__name__icontains=var) & Q(product__price__lte=30000)) 
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":var, })
    
            elif var1=="2":
                image  = Image.objects.filter(Q(product__sub__name__icontains=var) & Q(product__price__gte=30000))
        
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":var, })


            # filter by Brand 
            # else:
            #     image = Image.objects.filter(product__brand=var2)
            #     return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":var, "product":product})

          
    
        else:        
            
            image = Image.objects.all()    
            print("get3")
        
            return render(request, 'product/search.html', {"image":image, "dict1":dict1,})
               
               
        if 'brand' in request.GET:
            var2 = request.GET.get('brand')
            image = Image.objects.filter(product__brand=var2)
            return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":var, "product":brand_item})
            
    image = Image.objects.filter(Q(product__category__name__icontains=var)|Q(product__sub__name__icontains=var))
    
    
    if var == "":
            return render(request, 'product/search.html', {"image":image, "dict1":dict1,'query':var,})
    else: 
        return render(request, 'product/search.html', {"image":image, "dict1":dict1,'query':var, "product":brand_item})

    
  
  
  
        # if 'brand' in request.GET:
        #     # var = request.GET.get('search')
        #     var2 = request.GET.get('brand')
        #     print("second")
        #     print("var", var)
        #     print("var2",var2)
        #     image = Image.objects.filter(product__brand=var2)
        #     return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":var, "product":product})

        # else:        
            
        #     image = Image.objects.all()    
        #     print("get3")
        
        #     return render(request, 'product/search.html', {"image":image, "dict1":dict1,})
                       
                       
                       
# def search(request):
#     if request.method=='GET':
#         if 'search' in request.GET:
#            var = request.GET.get('search')
#            query  = request.GET.get('search')
#            query = "|".join(query.split(' '))
#            print(query)
#            search_query = SearchQuery(query, search_type='raw')

#            books = Image.objects.annotate(
#             search=SearchVector("product__brand","product__description","product__sub__name", "product__price", "product__brand", "product__category__name")
#                 ).filter(search=search_query).order_by('product__sub__name')
        
           
        
#         print(var)
            
#     return render(request, 'product/search.html', {"books":books, "query":query} )