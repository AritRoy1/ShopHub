from django.shortcuts import render, redirect
from django.views import View
from .forms import ProductUpdateForm, ProductAddForm, VendorRegistrationForm
from django.http import HttpResponse , HttpResponseRedirect
from .models import Product, Cart, Category, SubCategory, Image, Wishlist
from customer.models import Customer, Vendor
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery

from django.contrib.auth.decorators import login_required 
from payment.models import OrderDetail
from .forms import UpdateOrderForm
from django.core.paginator import Paginator



def VendorRegistration(request):
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST, request.FILES)
        # form = CustomerRegistrationForm(request.POST)
        if form.is_valid():     
            form.save()
            # return HttpResponseRedirect('/product/registration/')
            return HttpResponseRedirect('/login/')
             
    else:        
        form = VendorRegistrationForm()
        
    return render(request, 'product/vendor.html', {"form":form})


def vendor_pannel(request):
    print("jahan",request.user)
    approved = Vendor.objects.get(username = request.user)
    return render(request, 'product/vendor_base.html', {"approved":approved})


class ProductRegistration(View):
    def get(self, request):
        form =ProductUpdateForm
        return render(request, 'product/product.html', {"form":form})
    
    def post(self, request):
        form =ProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("sucessfully Submited")
        
               
def add_to_cart(request):
     
    user = request.user
    product_id = request.GET.get('prod_id')
    image = Image.objects.get(id = product_id)  
    product = Product.objects.get(image__id=product_id)  
    customer = Customer.objects.get(username = user)   
    cart = Cart(customer=customer,product=product, image=image) ## 1
    all_cart = Cart.objects.filter(customer__username=request.user)
  
    l1=[]
    for item in all_cart:
        l1.append(item.product)
   
    if product in l1:
        return redirect('/product/show-cart')
    else:
        cart.save() 
        return redirect('/product/show-cart') 
    

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
        user = request.user     
        customer = Customer.objects.get(username = user)    
        cart = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
        cart.quantity+=1
        cart.save()
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
        "quantity":cart.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)
        
def minus_cart(request):
    
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        user = request.user 
        customer = Customer.objects.get(username = user)     
        cart = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))      
        cart.quantity-=1
        if cart.quantity==0:
            cart.quantity=1
        cart.save()
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
        "quantity":cart.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)

       
def remove_cart(request):
    
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        user = request.user   
        customer = Customer.objects.get(username = user)        
        cart = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
     
        cart.delete()
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

## code for Search item 

# def search(request):
#     dict1={}
#     category = Category.objects.all()
#     for item in category:
#         dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
        
#     if request.method=='GET':
#         print("GET1")
        
#         if 'search' in request.GET:
           
#             print("----------------")
#             query = request.GET.get('search')
#             test = request.GET.get('test')           
#             print("var",query)
#             print("var1",test)          
                 
#             brand_item = Product.objects.filter(sub__name__icontains=query).distinct('brand')
#             color_item = Product.objects.filter(sub__name__icontains=query).distinct('color')
            
#             # filter by price
#             if test=='1':
#                 image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__lte=30000)) 
#                 return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
    
#             elif test=="2":
#                 image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__gte=30000))
        
#                 return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
    
#         else:            
#             image = Image.objects.all() 
#             return render(request, 'product/search.html', {"image":image, "dict1":dict1,})
               
#         # filter by brand
#         if 'brand' in request.GET:
#             var2 = request.GET.get('brand')
#             image = Image.objects.filter(product__brand=var2)
#             return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
#         # filter by color
#         if "color" in request.GET:
#             color = request.GET.get('color')
#             print(color)
#             image = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__color__icontains=color))
#             return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
#         # sort
#         if "sort" in request.GET:
#             sort = request.GET.get('sort')
#             print("sort",type(sort))
#             if sort=='1':
#                 image = Image.objects.filter(Q(product__sub__name__icontains=query)|Q(product__category__name__icontains=query)).order_by("product__price")
                
#                 return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
                
#             if sort=='2':
#                 image = Image.objects.filter(Q(product__sub__name__icontains=query)| Q (product__category__name__icontains=query)).order_by("-product__price")
#                 return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
                
            
#     image = Image.objects.filter(Q(product__category__name__icontains=query)|Q(product__sub__name__icontains=query))
        
#     if query == "":
#             return render(request, 'product/search.html', {"image":image, "dict1":dict1,'query':query,})
#     else: 
#         return render(request, 'product/search.html', {"image":image, "dict1":dict1,'query':query, "brand_item":brand_item,"color_item":color_item})

    
    
    
    
def wishlist(request):
    ## show all wishlist item 
    wishlist = Wishlist.objects.filter(customer__username = request.user)
    return render(request, 'product/wishlist.html', {"wishlist":wishlist})

def manage_products(request):
    approved = Vendor.objects.get(username = request.user)
    user = request.user
    images = Image.objects.filter(product__vendor__username=user)
    return render(request, 'product/vendor_products.html', {"images":images,"approved":approved})

# @login_required(login_url='login')
# def update_product_view(request,pk):
#     product=Product.objects.get(id=pk)
#     productForm=ProductForm(instance=product)
#     if request.method=='POST':
#         productForm=ProductForm(request.POST,request.FILES,instance=product)
#         if productForm.is_valid():
#             productForm.save()
#             return redirect('vendor-products')
#     return render(request,'product/vendor_update_product.html',{'productForm':productForm})


@login_required(login_url='login')
def update_product_view(request,pk, val):
    image = Image.objects.get(id=val)
    product = Product.objects.get(id=pk)    
    productForm=ProductUpdateForm(instance=product)
    if request.method=='POST':
        productForm=ProductUpdateForm(request.POST,request.FILES, instance=product)      
        if productForm.is_valid():
            productForm.save()
            if request.FILES:
                file =request.FILES['product_image']
                image.image = file
                image.save()          
            return redirect('manage-products')       
    return render(request,'product/vendor_update_product.html',{'productForm':productForm, 'img':image})

@login_required(login_url='login')
def delete_product_view(request,pk, val):
    product=Product.objects.get(id=pk)
    img = Image.objects.get(id=val)
    img.delete()
    product.delete()
    return redirect('manage-products')

def addProducts(request):
    productForm=ProductAddForm()
    # img = Image.objects.get()
    if request.method=='POST':
        productForm=ProductAddForm(request.POST, request.FILES)
        if productForm.is_valid():
            
            name = productForm.cleaned_data['name']
            description = productForm.cleaned_data['description']
            price = productForm.cleaned_data['price']
            brand = productForm.cleaned_data['brand']
            color = productForm.cleaned_data['color']
            category = productForm.cleaned_data['category']
            sub = productForm.cleaned_data['sub']
            
            vendor = Vendor.objects.get(username=request.user)
            product = Product(name=name,description=description, price=price,brand=brand, color=color,category=category, sub=sub, vendor=vendor)
            product.save()
            
    
            files =request.FILES['file']
            Image.objects.create(product = product, image=files)
            # productForm.save()
            return redirect('manage-products')
    return render(request,'product/vendor_add_products.html',{'productForm':productForm})

@login_required(login_url='login')
def view_Order(request):
    approved = Vendor.objects.get(username = request.user)
    order = OrderDetail.objects.filter(product__vendor__username=request.user)
    image = Image.objects.all()
    context ={
        'order':order,
        'image':image,
        'approved':approved
    }
    
    return render(request, 'product/vendor_looking_order.html', context)
    
def update_order_status(request, pk):
    print("pk",pk)
    instance = OrderDetail.objects.get(pk=pk)
    if request.method =="POST":
        print("jai")
        form = UpdateOrderForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('view-order')
        
    else:
        form = UpdateOrderForm(instance=instance)
    return render(request, 'product/update_status.html', {"form":form})

def delete_order_status(request, pk):
    order = OrderDetail.objects.get(pk=pk)
    order.delete()
    return redirect('view-order')



def search(request):
    dict1={}
    category = Category.objects.all()
    for item in category:
        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    if request.method=='GET':
        print("GET1")
        
        if 'search' in request.GET:
           
            print("----------------")
            query = request.GET.get('search')
            test = request.GET.get('test')           
            print("var",query)
            print("var1",test)          
                 
            brand_item = Product.objects.filter(sub__name__icontains=query).distinct('brand')
            color_item = Product.objects.filter(sub__name__icontains=query).distinct('color')
            
            # filter by price
            if test=='1':
                image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__lte=30000)) 
                paginator = Paginator(image, 3)
                page_number =  request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
    
            elif test=="2":
                image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__gte=30000))
        
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
    
        else:            
            image = Image.objects.all() 
            return render(request, 'product/search.html', {"image":image, "dict1":dict1,})
               
        # filter by brand
        if 'brand' in request.GET:
            var2 = request.GET.get('brand')
            image = Image.objects.filter(product__brand=var2)
            return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
        # filter by color
        if "color" in request.GET:
            color = request.GET.get('color')
            print(color)
            image = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__color__icontains=color))
            return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
        
        # sort
        if "sort" in request.GET:
            sort = request.GET.get('sort')
            print("sort",type(sort))
            if sort=='1':
                image = Image.objects.filter(Q(product__sub__name__icontains=query)|Q(product__category__name__icontains=query)).order_by("product__price")
                
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
                
            if sort=='2':
                image = Image.objects.filter(Q(product__sub__name__icontains=query)| Q (product__category__name__icontains=query)).order_by("-product__price")
                return render(request, 'product/search.html', {"image":image, "dict1":dict1, "query":query, "brand_item":brand_item, "color_item":color_item})
                
            
    image = Image.objects.filter(Q(product__category__name__icontains=query)|Q(product__sub__name__icontains=query)).order_by('id')
    paginator = Paginator(image, 3)
    page_number =  request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    if query == "":
            return render(request, 'product/search.html', {"image":page_obj, "dict1":dict1,'query':query,})
    else: 
        return render(request, 'product/search.html', {"image":page_obj, "dict1":dict1,'query':query, "brand_item":brand_item,"color_item":color_item})
