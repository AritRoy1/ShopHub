from django.shortcuts import render, redirect
from django.views import View
from .forms import ProductUpdateForm, ProductAddForm, VendorRegistrationForm, CancelOrderForm
from django.http import HttpResponse , HttpResponseRedirect
from .models import Product, Cart, Category, SubCategory, Image, Wishlist
from customer.models import Customer, Vendor
from django.db.models import Q
from django.db.models import Count

from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery

from django.contrib.auth.decorators import login_required 
from payment.models import OrderDetail
from .forms import UpdateOrderForm
from django.core.paginator import Paginator
from ratting.models import Ratting
from ShopHub import settings
from django.db.models import Avg
from django.views.generic import DetailView
from django.core.mail import send_mail
from datetime import datetime, date
from payment.models import OrderDetail
from django.db.models.functions import TruncWeek
from django.db.models import Sum


# vendor registration view
def VendorRegistration(request):
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():     
            form.save()
            return HttpResponseRedirect('/login/')
             
    else:        
        form = VendorRegistrationForm()     
    return render(request, 'product/vendor_registration_form.html', {"form":form})


# vendor redirect to vendor dashbord
def vendor_pannel(request):
    approved = Vendor.objects.get(username = request.user)
    return render(request, 'product/vendor_base.html', {"approved":approved})


# class ProductRegistration(View):
#     def get(self, request):
#         form =ProductUpdateForm
#         return render(request, 'product/product.html', {"form":form})
    
#     def post(self, request):
#         form =ProductUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("sucessfully Submited")
        
        
@login_required(login_url='login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    image = Image.objects.get(id = product_id)  
    product = Product.objects.get(image__id=product_id)  
    customer = Customer.objects.get(username = user)   
    cart = Cart(customer=customer,product=product, image=image) ## 1
    all_cart = Cart.objects.filter(customer__username=request.user)
  
    cart_list = []
    for item in all_cart:
        cart_list.append(item.product)
        
    # if the product is already in cart than redirect to show cart page 
    if product in cart_list:
        return redirect('/product/show-cart')
    else:
        
        # if the product is not in cart than save it and redirect to show cart page       
        cart.save() 
        return redirect('/product/show-cart') 
   
    
# after click cart in nav bar it show all cart if cart,  athorwise it gives empty cart
def show_cart(request):
    category = Category.objects.all()
    dict_category = {}
    for item in category:
        dict_category[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(customer=user) 
        amount = 0.0
        delivery_charges = 100
        total_amount = 0.0
        customer = Customer.objects.get(username=user)
        cart_product = [cart for cart in Cart.objects.all() if cart.customer == customer]
        
        if cart_product:
            for val in cart_product:
                tempamount = (val.quantity * val.product.price)
                amount +=tempamount
                total_amount = amount+delivery_charges
                   
            context = {      
                'carts':cart,
                'dict1':dict_category,
                'amount':amount, 
                'totalamount':total_amount,    
                }
            return render(request, 'product/add_to_cart.html', context)
        else:
            return render(request, "product/empty_cart.html")

    
# customer can add number of products in their cart
def add_cart(request): 
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        user = request.user     
        customer = Customer.objects.get(username = user)    
        cart = Cart.objects.get(Q(product__id=prod_id) & Q(customer__username=user))
        cart.quantity+=1
        cart.save()
        delivery_charges = 100
        amount = 0.0
        total_amount = 0.0     
        cart_product = [cart for cart in Cart.objects.all() if cart.customer == customer]
        for val in cart_product:
                tempamount = (val.quantity * val.product.price)
                amount += tempamount
                total_amount = amount+delivery_charges
    data = {
        "quantity":cart.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)
    
    
# customer can reduce products item form their cart    
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
        cart_product = [cart for cart in Cart.objects.all() if cart.customer == customer]
        for val in cart_product:
                tempamount = (val.quantity * val.product.price)
                amount +=tempamount
                total_amount = amount+delivery_charges
    data = {
        "quantity":cart.quantity,
        'amount':amount,
        'totalamount':total_amount
            
        }
    return JsonResponse(data)


# customer can remove/delete  products item form their cart        
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
                amount +=tempamount
                total_amount = amount+delivery_charges
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


# give all the list of products      
class ProductList(View):
    def get(self, request, pk):    
        category = Category.objects.all()
        subcatagory = SubCategory.objects.get(pk=pk)
        category = Category.objects.all()
        img = Image.objects.filter(product__sub__id=pk)
        dict_category={}   
        for item in category:

            dict_category[item.name] = SubCategory.objects.filter(category__name = item.name)
        context = {
            'dict1':dict_category,
            'subcatagory':subcatagory,
            "img":img,
            }
        return render(request, 'product/list_product.html', context)
        
# It gives the detail of one perticular product
class ProductDetail(View):
    def get(self, request, pk,prod_id):
        category = Category.objects.all()    
        stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        wishlist = Wishlist.objects.filter(customer__username=request.user)
        dict_category = {}
        for item in category:
            dict_category[item.name]=SubCategory.objects.filter(category__name = item.name)
                   
        products = Product.objects.get(id=prod_id)
        img = Image.objects.get(pk=pk)
        pro = img.product
        list_item=[]
        for item in wishlist:
            list_item.append(item.product)
            
        flag= False
        if pro in list_item:
            flag= True
        else:
            flag = False
        
        rattings = Ratting.objects.filter(product__image__id=pk).order_by('-id')[:5]
        average_rating = rattings.aggregate(Avg('ratting'))['ratting__avg']
        context = {"products":products,
                "img":img,
                'category':category, 
                'dict1':dict_category,
                "flag":flag, 
                "stripe_publishable_key":stripe_publishable_key,
                "average_rating":round(average_rating) if average_rating else 0,"rattings":rattings
                }
        return render(request, 'product/product_detail.html', context)

    
# vendor can manage their product
def manage_products(request):
    approved = Vendor.objects.get(username = request.user)
    user = request.user
    images = Image.objects.filter(product__vendor__username=user)
    context = {
        "images":images,
        "approved":approved     
    } 
    return render(request, 'product/vendor_products.html', context)

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


#vendor can update their products
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

# vendor can delete products
@login_required(login_url='login')
def delete_product_view(request,pk, val):
    product=Product.objects.get(id=pk)
    img = Image.objects.get(id=val)
    img.delete()
    product.delete()
    return redirect('manage-products')


# vendor can add products with multiple images
def addProducts(request):
    productForm=ProductAddForm()
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
            
            files = request.FILES.getlist('file')
            if files:
                for file in files:       
                    Image.objects.create(product = product, image=file)
            
            return redirect('manage-products')
    return render(request,'product/vendor_add_products.html',{'productForm':productForm})


# vendor can see how many orders  have come
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
 
 #######################################
 
def graph_Bar(request):
    # show how many product vendor have 
    product = Product.objects.filter(vendor__username = request.user)
    count_subcategory = {}
    for item in product:
       count_subcategory[item.sub] = count_subcategory.get(item.sub,0)+1
    
    # show per day product cell 
    today = datetime.utcnow().date()
    count_product_per_day = {}
    product_sub = OrderDetail.objects.filter(product__vendor__username=request.user, order_date__date = today)
    for item in product_sub:
        count_product_per_day[item.product.sub] = count_product_per_day.get(item.product.sub,0)+1
    
    # show profit chart
    amount = 0
    product_sub = OrderDetail.objects.filter(product__vendor__username=request.user, order_date__date = today)
    for product_amount in product_sub:
        amount += product_amount.amount
    print("amount", amount)
    
    ## practice
    # products_by_week = OrderDetail.objects.filter(product__vendor__username=request.user).annotate(
    #     week=TruncWeek('order_date')
    # ).values('week').annotate(total_quantity=Sum('amount'))
    
    
    
    orders_by_week = OrderDetail.objects.filter(product__vendor__username = request.user).annotate(
        week=TruncWeek('order_date')
    ).values('week').annotate(total_amount=Sum('amount'))
    print(orders_by_week)
    
    context = {
        "subcategory":count_subcategory,
        "count_product_per_day":count_product_per_day,
        "amount": amount,
        "products_by_week": orders_by_week,
    }
    return render(request, "product/vendor_graph.html", context)

##########################################

def update_order_status(request, pk):
    instance = OrderDetail.objects.get(pk=pk)
    if request.method =="POST":
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


# customer can search perticular product
def search(request):
    dict_category = {}
    category = Category.objects.all()
    for item in category:
        dict_category[item.name]=SubCategory.objects.filter(category__name = item.name)
        
    if request.method=='GET':  
        if 'search' in request.GET:
            query = request.GET.get('search')
            test = request.GET.get('test')                    
            brand_item = Product.objects.filter(sub__name__icontains=query).distinct('brand')
            color_item = Product.objects.filter(sub__name__icontains=query).distinct('color')
            
            # filter by price
            if test=='1':
                image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__lte=30000)) 
                context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
               
                return render(request, 'product/product_search.html', context)
    
            elif test=="2":
                image  = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__price__gte=30000))
                context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
        
                return render(request, 'product/product_search.html', context)

        else:            
            image = Image.objects.all() 
            context = {
                "image":image,
                "dict1":dict_category,     
            }
            return render(request, 'product/product_search.html',context)
               
        # filter by brand
        if 'brand' in request.GET:
            var2 = request.GET.get('brand')
            image = Image.objects.filter(product__brand=var2)
            context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
            return render(request, 'product/product_search.htmlearch.html', context)
        
        # filter by color
        if "color" in request.GET:
            color = request.GET.get('color')
            image = Image.objects.filter(Q(product__sub__name__icontains=query) & Q(product__color__icontains=color))
            context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
            return render(request, 'product/product_search.html', context )
        
        # sort
        if "sort" in request.GET:
            sort = request.GET.get('sort')
            if sort=='1':
                image = Image.objects.filter(Q(product__sub__name__icontains=query)|Q(product__category__name__icontains=query)).order_by("product__price")
                context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
                return render(request, 'product/product_search.html', context)
                
            if sort=='2':
                image = Image.objects.filter(Q(product__sub__name__icontains=query)| Q (product__category__name__icontains=query)).order_by("-product__price")
                context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
                return render(request, 'product/product_search.html', context)
                
            
    image = Image.objects.filter(Q(product__category__name__icontains=query)|Q(product__sub__name__icontains=query)).order_by('id')
        
    if query == "":
        context = {
            "image":image,
            "dict1":dict_category,
            'query':query,
        }
        return render(request, 'product/product_search.html', context)
    else: 
        context = {
                    "image":image,
                    "dict1":dict_category,
                    "query":query,
                    "brand_item":brand_item,
                    "color_item":color_item,
                }
        return render(request, 'product/product_search.html', context)



class TrackDetail(DetailView):
    model = Product
    template_name = "product/track_product.html"
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
  
# customer can see their order history   
class OrderHistoryView(View):
    def get(self, request):
        model = OrderDetail.objects.filter(customer__username=request.user)
        return render(request, 'product/order_history.html', {"object_list":model})
      
# customer can cancel there order 
class CancelOrder(View):
    def get(self, request, product_id, image_id, order_id ):
      image = Image.objects.get(pk=image_id)  
      form = CancelOrderForm()
      return render(request, 'product/order_cancel.html', {"form":form, "image":image})
      
    def post(self, request, product_id, image_id, order_id):   
      form = CancelOrderForm(request.POST)
      order = OrderDetail.objects.get(id=order_id)
      if form.is_valid():  
        order.has_paid=False
        order.save()  
        
        # send mail to customer after successfully cancel order
        subject = 'Order Cancel'
        message = f'Your order has been cancel .. Your Paymnet will send to your account within 5 to 6 working day'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['request.user.email' ]   
        send_mail( subject, message, email_from, recipient_list ) 
        return render(request,'product/order_cancel_successfully.html')