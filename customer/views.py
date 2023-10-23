from django.shortcuts import render, redirect
from django.http import HttpResponse , HttpResponseRedirect 
from .models import Customer, Vendor
from .forms import CustomerRegistrationForm, VendorRegistrationForm
from django.views import View
from django.contrib.auth import authenticate, login , logout
from .forms import LoginForm
from django. contrib import messages
from product.models import Category, Image, Product, SubCategory



def home(request):
    category = Category.objects.all()
    subcatagory = SubCategory.objects.all()   
    image = Image.objects.all()
    # image1 = Image.objects.filter()
    
    dict1={}
    dict2={}
    for item in category:

        dict1[item.name]=SubCategory.objects.filter(category__name = item.name)    
    
    for sub in subcatagory:
        dict2[sub.name]=Image.objects.filter(product__sub__name=sub.name)
    print(dict2)
    
    return render(request, 'customer/home.html', {'category':category, "dict1":dict1, "dict2":dict2,  'image':image, 'subactegory':subcatagory})

def CustomerRegistration(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        # form = CustomerRegistrationForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect('/login/')
                 
    else:    
        form = CustomerRegistrationForm()
    return render(request, 'customer/customer.html', {"form":form})

def VendorRegistration(request):
    if request.method == "POST":
        form = VendorRegistrationForm(request.POST, request.FILES)
        # form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            return HttpResponseRedirect('/product/registration/')
        
      
    else:
          
        form = VendorRegistrationForm()
    return render(request, 'customer/vendor.html', {"form":form})


class Login(View):
    def get(self, request):
        form =LoginForm
        return render(request, 'customer/login.html', {"form":form})
    def post(self, request):
        form =LoginForm(request.POST)      
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
        
            User = authenticate(request, username=username, password=password)  
            
            if User is not None:
                login(request, User)
                
                return HttpResponseRedirect('/home/')      
            else:
                messages.info(request, 'username or password is wrong')

        else :
          return HttpResponse("dfghjk")
      
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
       
        
class ProductList(View):
    def get(self, request, pk):
        
        category = Category.objects.all()
        subcatagory = SubCategory.objects.get(pk=pk)
        phone = Product.objects.filter(id=1)
        category = Category.objects.all()
        img = Image.objects.filter(product__sub__id=pk)
        dict1={}
        
        for item in category:

            dict1[item.name]=SubCategory.objects.filter(category__name = item.name)

        return render(request, 'customer/list_product.html', {'dict1':dict1, 'subcatagory':subcatagory, "img":img,})
        
        
        # return render(request, 'customer/list_product.html', {'dict1':dict1,
        #                 "phone":phone, "img":img, 'category':category, 'subcatagory':subcatagory})


class ProductDetail(View):
    def get(self, request, pk):
        category = Category.objects.all()
        dict1={}
        for item in category:
            dict1[item.name]=SubCategory.objects.filter(category__name = item.name)
            
        print(pk)   
        
        phone = Product.objects.filter(id=pk)
        
        img = Image.objects.get(pk=pk)
        return render(request, 'customer/product_detail.html', {"phone":phone,
                "img":img, 'category':category, 'dict1':dict1})

