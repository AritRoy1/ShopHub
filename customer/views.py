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
    
    
    return render(request, 'customer/home.html', {'category':category})

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

  
     
class ProductDetail(View):
    def get(self, request):
        phone = Product.objects.filter(id=1)
        category = Category.objects.all()
        img = Image.objects.all()
        return render(request, 'customer/electronics.html', {"phone":phone, "img":img, 'category':category})